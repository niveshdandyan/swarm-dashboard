"""
Swarm Dashboard - Live real-time dashboard for monitoring AI agent swarms.

A self-contained Python server with embedded HTML/CSS/JS for monitoring
AI agent swarms. Features include:

- Real-time updates via polling
- Smart completion detection
- Capybara-inspired color palette
- Light/dark theme toggle
- Clickable agent detail panels
- Live activity feed
- Zero external dependencies
"""

from swarm_dashboard.agents import AgentStatusManager
from swarm_dashboard.config import AgentConfig, Config
from swarm_dashboard.launcher import (
    create_agent_output_symlink,
    find_task_output_file,
    launch_dashboard,
    stop_dashboard,
    update_agent_task_id,
)
from swarm_dashboard.parser import (
    extract_files_created,
    extract_live_events,
    extract_tool_usage,
    parse_json_lines,
)
from swarm_dashboard.server import DashboardHandler, DashboardServer
from swarm_dashboard.tracker import BoundedParseCache, FilePositionTracker

__version__ = "6.1.0"
__author__ = "HappyCapy"
__license__ = "MIT"

__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__license__",
    # Config
    "Config",
    "AgentConfig",
    # Tracking
    "FilePositionTracker",
    "BoundedParseCache",
    # Parsing
    "parse_json_lines",
    "extract_tool_usage",
    "extract_live_events",
    "extract_files_created",
    # Agents
    "AgentStatusManager",
    # Server
    "DashboardServer",
    "DashboardHandler",
    # Launcher
    "launch_dashboard",
    "update_agent_task_id",
    "stop_dashboard",
    "find_task_output_file",
    "create_agent_output_symlink",
]
