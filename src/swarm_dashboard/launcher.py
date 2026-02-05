"""
Dashboard launcher utilities for Swarm Dashboard.

This module provides functions for launching and managing the dashboard
server, including automatic port selection, configuration creation,
and output file symlink management.
"""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from swarm_dashboard.config import AgentConfig, Config

# Port configuration
DEFAULT_PORT = 8080
PORT_RANGE_START = 8081
PORT_RANGE_END = 8089
FALLBACK_RANGE_START = 8090
FALLBACK_RANGE_END = 9000


def is_port_available(port: int) -> bool:
    """
    Check if a port is available for binding.

    Args:
        port: Port number to check.

    Returns:
        True if port is available, False otherwise.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", port))
            return True
        except OSError:
            return False


def select_port(preferred: int = DEFAULT_PORT) -> int:
    """
    Select an available port for the dashboard.

    Priority:
    1. Preferred port (default 8080)
    2. Alternative ports 8081-8089
    3. Random available port in range 8090-9000

    Args:
        preferred: Preferred port number.

    Returns:
        Available port number.

    Raises:
        RuntimeError: If no port is available.
    """
    if is_port_available(preferred):
        return preferred

    for port in range(PORT_RANGE_START, PORT_RANGE_END + 1):
        if is_port_available(port):
            return port

    for port in range(FALLBACK_RANGE_START, FALLBACK_RANGE_END):
        if is_port_available(port):
            return port

    raise RuntimeError("No available ports for dashboard")


def find_task_output_file(
    task_id: str, task_dir: Optional[str] = None
) -> Optional[str]:
    """
    Find the output file for a task ID.

    Searches common locations for Claude Code task output files.

    Args:
        task_id: The task ID to find output for.
        task_dir: Optional explicit task directory.

    Returns:
        Path to output file if found, None otherwise.
    """
    search_paths = []

    if task_dir:
        search_paths.append(os.path.join(task_dir, f"{task_id}.output"))

    # Check environment variable
    env_task_dir = os.getenv("TASK_DIR")
    if env_task_dir:
        search_paths.insert(0, os.path.join(env_task_dir, f"{task_id}.output"))

    # Standard Claude Code task directories
    search_paths.extend(
        [
            f"/tmp/claude-tasks/{task_id}.output",
            f"/tmp/claude-1000/{task_id}.output",
            os.path.expanduser(f"~/.claude/tasks/{task_id}.output"),
        ]
    )

    for path in search_paths:
        if os.path.exists(path):
            return path

    return None


def create_agent_output_symlink(
    swarm_dir: str,
    agent_id: str,
    task_id: str,
    task_dir: Optional[str] = None,
) -> Optional[str]:
    """
    Create a symlink from agent directory to task output file.

    This enables the dashboard to find and parse live activity data
    for each agent by looking in a predictable location.

    Args:
        swarm_dir: Base directory for the swarm.
        agent_id: Agent identifier (e.g., "agent-1-core").
        task_id: Task ID returned from Task tool.
        task_dir: Optional explicit task directory.

    Returns:
        Path to created symlink, or None if creation failed.
    """
    # Create agent directory
    agent_dir = os.path.join(swarm_dir, agent_id)
    Path(agent_dir).mkdir(parents=True, exist_ok=True)

    # Find actual output file
    output_file = find_task_output_file(task_id, task_dir)

    if not output_file:
        # Create placeholder path
        if task_dir:
            output_file = os.path.join(task_dir, f"{task_id}.output")
        else:
            output_file = f"/tmp/claude-tasks/{task_id}.output"

    # Create symlink
    symlink_path = os.path.join(agent_dir, "output.jsonl")

    # Remove existing
    if os.path.islink(symlink_path):
        os.unlink(symlink_path)
    elif os.path.exists(symlink_path):
        os.remove(symlink_path)

    try:
        os.symlink(output_file, symlink_path)
        return symlink_path
    except OSError:
        return None


def update_agent_task_id(
    swarm_dir: str,
    agent_id: str,
    task_id: str,
    task_dir: Optional[str] = None,
    create_symlink: bool = True,
) -> None:
    """
    Update an agent's task_id in swarm-config.json and create output symlink.

    Call this after launching each agent to record its task ID and enable
    live activity tracking in the dashboard.

    Args:
        swarm_dir: Base directory for the swarm.
        agent_id: Agent identifier (e.g., "agent-1-core").
        task_id: Task ID returned from Task tool.
        task_dir: Optional explicit task directory for output files.
        create_symlink: Whether to create symlink to output file.

    Example:
        >>> update_agent_task_id(
        ...     swarm_dir="/workspace/my-project",
        ...     agent_id="agent-1-core",
        ...     task_id="abc123def456"
        ... )
    """
    config_path = os.path.join(swarm_dir, "swarm-config.json")

    with open(config_path) as f:
        config = json.load(f)

    if agent_id in config.get("agents", {}):
        config["agents"][agent_id]["task_id"] = task_id
        config["agents"][agent_id]["status"] = "in_progress"
        config["agents"][agent_id]["started_at"] = (
            datetime.utcnow().isoformat() + "Z"
        )

        if task_dir:
            config["task_dir"] = task_dir

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    # Create symlink
    if create_symlink:
        symlink_path = create_agent_output_symlink(
            swarm_dir, agent_id, task_id, task_dir or config.get("task_dir")
        )
        if symlink_path:
            with open(config_path) as f:
                config = json.load(f)
            if agent_id in config.get("agents", {}):
                config["agents"][agent_id]["output_symlink"] = symlink_path
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)


def launch_dashboard(
    swarm_name: str,
    swarm_dir: str,
    agents: Dict[str, Dict[str, Any]],
    port: int = DEFAULT_PORT,
) -> str:
    """
    Launch dashboard server and return URL.

    This is the main entry point for launching the swarm dashboard.
    It handles:
    1. Creating swarm-config.json with agent registry
    2. Starting the dashboard server in background
    3. Returning the dashboard URL

    Args:
        swarm_name: Name of the swarm/project.
        swarm_dir: Base directory for the swarm workspace.
        agents: Dictionary of agent configurations.
        port: Preferred port number.

    Returns:
        Dashboard URL string.

    Example:
        >>> url = launch_dashboard(
        ...     swarm_name="my-project",
        ...     swarm_dir="/workspace/my-project",
        ...     agents={
        ...         "agent-1-core": {"role": "Core", "wave": 1, "mission": "Setup"},
        ...     }
        ... )
        >>> print(url)
        http://localhost:8080/
    """
    # Ensure directory exists
    Path(swarm_dir).mkdir(parents=True, exist_ok=True)

    # Select port
    selected_port = select_port(port)

    # Create config
    config = Config(
        swarm_name=swarm_name,
        swarm_dir=swarm_dir,
        task_dir=swarm_dir,
        port=selected_port,
        start_time=datetime.utcnow().isoformat() + "Z",
    )

    for agent_id, agent_data in agents.items():
        config.agents[agent_id] = AgentConfig(
            role=agent_data.get("role", agent_id),
            wave=agent_data.get("wave", 1),
            task_id=agent_data.get("task_id"),
            mission=agent_data.get("mission", ""),
        )

    config.save()

    # Start server in background
    server_module = "swarm_dashboard.server"
    process = subprocess.Popen(
        [
            sys.executable,
            "-c",
            f"from {server_module} import run_server; "
            f"from swarm_dashboard.config import Config; "
            f"config = Config.from_file('{config.get_config_path()}'); "
            f"run_server(config)",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,
    )

    # Wait for startup
    time.sleep(0.5)

    if process.poll() is not None:
        stderr = process.stderr.read().decode() if process.stderr else ""
        raise RuntimeError(f"Dashboard server failed to start: {stderr}")

    # Save PID
    pid_path = os.path.join(swarm_dir, ".dashboard.pid")
    with open(pid_path, "w") as f:
        f.write(str(process.pid))

    # Set environment
    os.environ["SWARM_DASHBOARD_PORT"] = str(selected_port)

    return f"http://localhost:{selected_port}/"


def stop_dashboard(swarm_dir: str) -> bool:
    """
    Stop the dashboard server.

    Args:
        swarm_dir: Base directory for the swarm.

    Returns:
        True if server was stopped, False if not running.
    """
    pid_path = os.path.join(swarm_dir, ".dashboard.pid")

    if not os.path.exists(pid_path):
        return False

    try:
        with open(pid_path) as f:
            pid = int(f.read().strip())

        os.kill(pid, 15)  # SIGTERM
        os.remove(pid_path)
        return True
    except (ProcessLookupError, ValueError, FileNotFoundError):
        return False
