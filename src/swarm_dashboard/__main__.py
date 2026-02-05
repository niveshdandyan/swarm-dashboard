"""
Module entry point for running swarm-dashboard as a module.

Usage:
    python -m swarm_dashboard serve
    python -m swarm_dashboard launch --name "My Swarm" --dir /workspace
"""

import sys

from swarm_dashboard.cli import main

if __name__ == "__main__":
    sys.exit(main())
