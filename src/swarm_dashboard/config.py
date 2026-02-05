"""
Configuration management for Swarm Dashboard.

This module provides configuration classes and utilities for managing
dashboard settings, agent configurations, and runtime parameters.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

# Default configuration values
DEFAULT_PORT = 8080
DEFAULT_SWARM_DIR = "/workspace/project"
DEFAULT_TASK_DIR = "/tmp/claude-1000"
DEFAULT_SWARM_NAME = "Agent Swarm"

# Thresholds
IDLE_THRESHOLD_SECONDS = 60
COMPLETION_THRESHOLD_SECONDS = 120

# Cache settings
MAX_CACHE_SIZE = 50
MAX_LIVE_EVENTS = 30
MAX_CONTENT_LENGTH = 200

# Completion markers that indicate an agent has finished
COMPLETION_MARKERS: List[str] = [
    "EVOLUTION COMPLETE",
    "Task completed",
    "All tasks completed",
    'status": "completed"',
    "Successfully completed",
    "Finished all",
    "COMPLETED",
    "Done!",
]


@dataclass
class AgentConfig:
    """Configuration for a single agent in the swarm."""

    role: str
    wave: int = 1
    task_id: Optional[str] = None
    mission: str = ""
    status: str = "pending"
    progress: int = 0
    files_created: List[str] = field(default_factory=list)
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    output_symlink: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> AgentConfig:
        """Create an AgentConfig from a dictionary."""
        return cls(
            role=data.get("role", "Unknown"),
            wave=data.get("wave", 1),
            task_id=data.get("task_id"),
            mission=data.get("mission", ""),
            status=data.get("status", "pending"),
            progress=data.get("progress", 0),
            files_created=data.get("files_created", []),
            started_at=data.get("started_at"),
            completed_at=data.get("completed_at"),
            output_symlink=data.get("output_symlink"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "role": self.role,
            "wave": self.wave,
            "task_id": self.task_id,
            "mission": self.mission,
            "status": self.status,
            "progress": self.progress,
            "files_created": self.files_created,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "output_symlink": self.output_symlink,
        }


@dataclass
class Config:
    """Main configuration for the Swarm Dashboard."""

    swarm_name: str = DEFAULT_SWARM_NAME
    swarm_dir: str = DEFAULT_SWARM_DIR
    task_dir: str = DEFAULT_TASK_DIR
    port: int = DEFAULT_PORT
    start_time: Optional[str] = None
    agents: Dict[str, AgentConfig] = field(default_factory=dict)

    # Thresholds
    idle_threshold: int = IDLE_THRESHOLD_SECONDS
    completion_threshold: int = COMPLETION_THRESHOLD_SECONDS

    # Cache settings
    max_cache_size: int = MAX_CACHE_SIZE
    max_live_events: int = MAX_LIVE_EVENTS
    max_content_length: int = MAX_CONTENT_LENGTH

    @classmethod
    def from_env(cls) -> Config:
        """Create configuration from environment variables."""
        return cls(
            swarm_name=os.getenv("SWARM_NAME", DEFAULT_SWARM_NAME),
            swarm_dir=os.getenv("SWARM_DIR", DEFAULT_SWARM_DIR),
            task_dir=os.getenv("TASK_DIR", DEFAULT_TASK_DIR),
            port=int(os.getenv("DASHBOARD_PORT", str(DEFAULT_PORT))),
        )

    @classmethod
    def from_file(cls, config_path: str) -> Config:
        """Load configuration from a JSON file."""
        with open(config_path, encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Config:
        """Create configuration from a dictionary."""
        agents = {}
        for agent_id, agent_data in data.get("agents", {}).items():
            agents[agent_id] = AgentConfig.from_dict(agent_data)

        return cls(
            swarm_name=data.get("swarm_name", DEFAULT_SWARM_NAME),
            swarm_dir=data.get("swarm_dir", DEFAULT_SWARM_DIR),
            task_dir=data.get("task_dir", DEFAULT_TASK_DIR),
            port=data.get("dashboard", {}).get("port", DEFAULT_PORT),
            start_time=data.get("start_time"),
            agents=agents,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "swarm_name": self.swarm_name,
            "swarm_dir": self.swarm_dir,
            "task_dir": self.task_dir,
            "start_time": self.start_time,
            "dashboard": {
                "port": self.port,
                "refresh_interval": 5000,
                "auto_open_browser": False,
            },
            "agents": {
                agent_id: agent.to_dict() for agent_id, agent in self.agents.items()
            },
        }

    def save(self, config_path: Optional[str] = None) -> str:
        """Save configuration to a JSON file."""
        if config_path is None:
            config_path = os.path.join(self.swarm_dir, "swarm-config.json")

        Path(config_path).parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

        return config_path

    def get_config_path(self) -> str:
        """Get the path to the swarm-config.json file."""
        return os.path.join(self.swarm_dir, "swarm-config.json")

    def load_from_swarm_dir(self) -> Config:
        """Reload configuration from the swarm directory."""
        config_path = self.get_config_path()
        if os.path.exists(config_path):
            return Config.from_file(config_path)
        return self
