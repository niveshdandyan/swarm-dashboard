"""
Agent status management for Swarm Dashboard.

This module provides the AgentStatusManager class for tracking and
managing the status of agents in a swarm, including status detection,
progress tracking, and activity monitoring.
"""

from __future__ import annotations

import glob
import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from swarm_dashboard.config import (
    COMPLETION_THRESHOLD_SECONDS,
    Config,
    IDLE_THRESHOLD_SECONDS,
)
from swarm_dashboard.parser import (
    format_time_ago,
    get_file_mtime,
    parse_agent_output,
    read_json_file,
)

logger = logging.getLogger(__name__)


class AgentStatusManager:
    """
    Manages agent status detection and tracking.

    This class handles:
    - Loading agent configurations from swarm-config.json
    - Detecting agent status (pending, running, idle, completed, failed)
    - Tracking agent progress and activity
    - Finding agent output files

    Example:
        manager = AgentStatusManager(config)
        status = manager.get_swarm_status()
        agent_details = manager.get_agent_details("agent-1")
    """

    def __init__(self, config: Config) -> None:
        """
        Initialize the agent status manager.

        Args:
            config: Swarm configuration object.
        """
        self.config = config
        self._start_time = datetime.utcnow().isoformat() + "Z"

    def get_swarm_status(self) -> Dict[str, Any]:
        """
        Get the overall swarm status.

        Returns:
            Dictionary with swarm name, start time, agent counts,
            overall progress, and per-agent status.
        """
        # Reload config to get latest agent data
        config = self._load_config()

        agents_status: Dict[str, Dict[str, Any]] = {}
        completed = 0
        running = 0
        idle = 0
        failed = 0
        pending = 0

        for agent_id, agent_config in config.agents.items():
            status = self._get_agent_status(agent_id, agent_config)
            agents_status[agent_id] = status

            # Count by status
            agent_status = status.get("status", "pending")
            if agent_status == "completed":
                completed += 1
            elif agent_status == "running":
                running += 1
            elif agent_status == "idle":
                idle += 1
            elif agent_status == "failed":
                failed += 1
            else:
                pending += 1

        total = len(agents_status)
        overall_progress = int((completed / total * 100)) if total > 0 else 0

        return {
            "swarm_name": config.swarm_name,
            "start_time": config.start_time or self._start_time,
            "last_updated": datetime.utcnow().isoformat() + "Z",
            "overall_progress": overall_progress,
            "completed_count": completed,
            "running_count": running,
            "idle_count": idle,
            "failed_count": failed,
            "pending_count": pending,
            "total_agents": total,
            "agents": agents_status,
        }

    def get_agent_details(self, agent_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific agent.

        Args:
            agent_id: The agent identifier.

        Returns:
            Dictionary with full agent details including live events,
            tool usage, files created, etc.
        """
        config = self._load_config()

        if agent_id not in config.agents:
            return {"error": f"Agent {agent_id} not found"}

        agent_config = config.agents[agent_id]
        output_file = self._find_agent_output(agent_id, agent_config)
        parsed = parse_agent_output(output_file)

        # Determine status
        status_data = self._get_agent_status(agent_id, agent_config)

        return {
            "id": agent_id,
            "role": agent_config.role,
            "mission": agent_config.mission,
            "wave": agent_config.wave,
            "status": status_data.get("status", "pending"),
            "progress": status_data.get("progress", 0),
            "files_created": parsed.get("files_created", []),
            "tools_used": parsed.get("tools_used", {}),
            "total_events": parsed.get("total_events", 0),
            "last_activity": status_data.get("last_activity"),
            "last_activity_ago": status_data.get("last_activity_ago", "Unknown"),
            "is_idle": status_data.get("is_idle", False),
            "live_events": parsed.get("live_events", []),
        }

    def _load_config(self) -> Config:
        """Load the current configuration from file."""
        config_path = self.config.get_config_path()
        if os.path.exists(config_path):
            try:
                return Config.from_file(config_path)
            except Exception as e:
                logger.error(f"Error loading config: {e}")
        return self.config

    def _get_agent_status(
        self, agent_id: str, agent_config: Any
    ) -> Dict[str, Any]:
        """
        Determine the status of a single agent.

        Status detection priority:
        1. status.json file in agent directory
        2. Completion markers in output
        3. Idle time thresholds
        """
        result: Dict[str, Any] = {
            "role": agent_config.role,
            "status": "pending",
            "progress": 0,
            "activity": "",
            "wave": agent_config.wave,
            "last_activity": None,
            "last_activity_ago": "Unknown",
            "is_idle": False,
            "tools_used": {},
        }

        # Check for status.json in agent directory
        agent_dir = os.path.join(self.config.swarm_dir, agent_id)
        status_file = os.path.join(agent_dir, "status.json")

        if os.path.exists(status_file):
            status_data = read_json_file(status_file)
            if status_data:
                result["status"] = status_data.get("status", "pending")
                result["progress"] = status_data.get("progress", 0)
                result["files_created"] = status_data.get("files_created", [])

                if result["status"] == "completed":
                    result["progress"] = 100
                    return result

        # Find and parse output file
        output_file = self._find_agent_output(agent_id, agent_config)

        if not output_file or not os.path.exists(output_file):
            return result

        # Parse output
        parsed = parse_agent_output(output_file)

        result["tools_used"] = parsed.get("tools_used", {})
        result["activity"] = parsed.get("activity", "")
        result["progress"] = parsed.get("progress", 0)

        # Get last activity time
        last_activity = parsed.get("last_activity") or get_file_mtime(output_file)
        result["last_activity"] = (
            last_activity.isoformat() if last_activity else None
        )
        result["last_activity_ago"] = format_time_ago(last_activity)

        # Determine status based on completion and idle time
        if parsed.get("is_complete"):
            result["status"] = "completed"
            result["progress"] = 100
        elif last_activity:
            now = datetime.now(timezone.utc)
            seconds_idle = (now - last_activity).total_seconds()

            if seconds_idle > COMPLETION_THRESHOLD_SECONDS:
                result["status"] = "completed"
                result["progress"] = 100
            elif seconds_idle > IDLE_THRESHOLD_SECONDS:
                result["status"] = "idle"
                result["is_idle"] = True
            else:
                result["status"] = "running"
        else:
            result["status"] = "running"

        return result

    def _find_agent_output(
        self, agent_id: str, agent_config: Any
    ) -> Optional[str]:
        """
        Find the output file for an agent.

        Searches in order:
        1. Symlink in agent directory (output.jsonl)
        2. Task output file using task_id
        3. Common output file patterns in agent directory
        """
        agent_dir = os.path.join(self.config.swarm_dir, agent_id)

        # Check for symlink (preferred method)
        symlink_path = os.path.join(agent_dir, "output.jsonl")
        if os.path.exists(symlink_path):
            return symlink_path

        # Check task_id based path
        task_id = agent_config.task_id
        if task_id:
            possible_paths = [
                os.path.join(self.config.task_dir, f"{task_id}.output"),
                f"/tmp/claude-tasks/{task_id}.output",
                f"/tmp/claude-1000/{task_id}.output",
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    return path

        # Check common patterns in agent directory
        patterns = [
            os.path.join(agent_dir, "output.jsonl"),
            os.path.join(agent_dir, "agent.output"),
            os.path.join(agent_dir, "*.output"),
            os.path.join(agent_dir, "*.jsonl"),
        ]

        for pattern in patterns:
            matches = glob.glob(pattern)
            if matches:
                return matches[0]

        return None

    def get_agents_by_wave(self) -> Dict[int, List[str]]:
        """
        Group agents by their wave number.

        Returns:
            Dictionary mapping wave numbers to lists of agent IDs.
        """
        config = self._load_config()
        waves: Dict[int, List[str]] = {}

        for agent_id, agent_config in config.agents.items():
            wave = agent_config.wave
            if wave not in waves:
                waves[wave] = []
            waves[wave].append(agent_id)

        return waves
