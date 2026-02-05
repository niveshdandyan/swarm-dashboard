"""
Command-line interface for Swarm Dashboard.

Provides CLI commands for starting the server, managing configuration,
and controlling the dashboard lifecycle.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from typing import Optional

from swarm_dashboard.config import Config
from swarm_dashboard.launcher import launch_dashboard, stop_dashboard
from swarm_dashboard.server import run_server


def setup_logging(verbose: bool = False) -> None:
    """Configure logging based on verbosity."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def cmd_serve(args: argparse.Namespace) -> int:
    """Run the dashboard server."""
    setup_logging(args.verbose)

    # Load config
    if args.config:
        config = Config.from_file(args.config)
    else:
        config = Config.from_env()

    # Override with CLI args
    if args.port:
        config.port = args.port
    if args.swarm_dir:
        config.swarm_dir = args.swarm_dir

    run_server(config)
    return 0


def cmd_launch(args: argparse.Namespace) -> int:
    """Launch dashboard in background."""
    setup_logging(args.verbose)

    try:
        agents = json.loads(args.agents) if args.agents else {}
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON for agents: {e}", file=sys.stderr)
        return 1

    try:
        url = launch_dashboard(
            swarm_name=args.name,
            swarm_dir=args.dir,
            agents=agents,
            port=args.port,
        )
        print(f"Dashboard launched: {url}")
        return 0
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_stop(args: argparse.Namespace) -> int:
    """Stop running dashboard."""
    if stop_dashboard(args.dir):
        print("Dashboard stopped")
        return 0
    else:
        print("Dashboard was not running")
        return 1


def cmd_status(args: argparse.Namespace) -> int:
    """Check dashboard status."""
    import os

    pid_path = os.path.join(args.dir, ".dashboard.pid")

    if not os.path.exists(pid_path):
        print("Dashboard is not running")
        return 1

    try:
        with open(pid_path) as f:
            pid = int(f.read().strip())

        # Check if process exists
        os.kill(pid, 0)
        print(f"Dashboard is running (PID: {pid})")
        return 0
    except (ProcessLookupError, ValueError):
        print("Dashboard is not running (stale PID file)")
        return 1


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="swarm-dashboard",
        description="Live real-time dashboard for monitoring AI agent swarms",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 6.1.0",
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # serve command
    serve_parser = subparsers.add_parser(
        "serve",
        help="Run the dashboard server",
    )
    serve_parser.add_argument(
        "-c", "--config",
        help="Path to swarm-config.json",
    )
    serve_parser.add_argument(
        "-p", "--port",
        type=int,
        help="Server port",
    )
    serve_parser.add_argument(
        "-d", "--swarm-dir",
        help="Swarm directory",
    )
    serve_parser.set_defaults(func=cmd_serve)

    # launch command
    launch_parser = subparsers.add_parser(
        "launch",
        help="Launch dashboard in background",
    )
    launch_parser.add_argument(
        "-n", "--name",
        required=True,
        help="Swarm/project name",
    )
    launch_parser.add_argument(
        "-d", "--dir",
        required=True,
        help="Swarm directory path",
    )
    launch_parser.add_argument(
        "-p", "--port",
        type=int,
        default=8080,
        help="Preferred port",
    )
    launch_parser.add_argument(
        "-a", "--agents",
        default="{}",
        help="Agent configuration as JSON string",
    )
    launch_parser.set_defaults(func=cmd_launch)

    # stop command
    stop_parser = subparsers.add_parser(
        "stop",
        help="Stop running dashboard",
    )
    stop_parser.add_argument(
        "-d", "--dir",
        required=True,
        help="Swarm directory path",
    )
    stop_parser.set_defaults(func=cmd_stop)

    # status command
    status_parser = subparsers.add_parser(
        "status",
        help="Check dashboard status",
    )
    status_parser.add_argument(
        "-d", "--dir",
        required=True,
        help="Swarm directory path",
    )
    status_parser.set_defaults(func=cmd_status)

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        # Default to serve command with env config
        args.config = None
        args.port = None
        args.swarm_dir = None
        args.verbose = getattr(args, "verbose", False)
        return cmd_serve(args)

    result: int = args.func(args)
    return result


if __name__ == "__main__":
    sys.exit(main())
