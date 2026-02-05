"""Tests for configuration module."""

import json
import os

import pytest

from swarm_dashboard.config import AgentConfig, Config


class TestAgentConfig:
    """Tests for AgentConfig dataclass."""

    def test_create_agent_config(self):
        """Test creating an agent config."""
        config = AgentConfig(
            role="Test Agent",
            wave=1,
            mission="Test mission",
        )
        assert config.role == "Test Agent"
        assert config.wave == 1
        assert config.mission == "Test mission"
        assert config.status == "pending"
        assert config.progress == 0

    def test_from_dict(self):
        """Test creating config from dictionary."""
        data = {
            "role": "Backend Developer",
            "wave": 2,
            "task_id": "abc123",
            "mission": "Build API",
            "status": "running",
            "progress": 50,
        }
        config = AgentConfig.from_dict(data)
        assert config.role == "Backend Developer"
        assert config.wave == 2
        assert config.task_id == "abc123"
        assert config.status == "running"
        assert config.progress == 50

    def test_to_dict(self):
        """Test converting config to dictionary."""
        config = AgentConfig(
            role="Test Agent",
            wave=1,
            task_id="xyz789",
            mission="Test mission",
        )
        data = config.to_dict()
        assert data["role"] == "Test Agent"
        assert data["wave"] == 1
        assert data["task_id"] == "xyz789"
        assert data["mission"] == "Test mission"


class TestConfig:
    """Tests for Config dataclass."""

    def test_create_config(self, temp_dir):
        """Test creating a config."""
        config = Config(
            swarm_name="My Swarm",
            swarm_dir=temp_dir,
            task_dir=temp_dir,
            port=8080,
        )
        assert config.swarm_name == "My Swarm"
        assert config.port == 8080

    def test_from_env(self, monkeypatch):
        """Test creating config from environment variables."""
        monkeypatch.setenv("SWARM_NAME", "Env Swarm")
        monkeypatch.setenv("SWARM_DIR", "/test/swarm")
        monkeypatch.setenv("DASHBOARD_PORT", "9000")

        config = Config.from_env()
        assert config.swarm_name == "Env Swarm"
        assert config.swarm_dir == "/test/swarm"
        assert config.port == 9000

    def test_save_and_load(self, temp_dir):
        """Test saving and loading config."""
        config = Config(
            swarm_name="Save Test",
            swarm_dir=temp_dir,
            task_dir=temp_dir,
            port=8080,
        )
        config.agents["agent-1"] = AgentConfig(
            role="Test Agent",
            wave=1,
            mission="Test",
        )

        # Save
        config_path = config.save()
        assert os.path.exists(config_path)

        # Load
        loaded = Config.from_file(config_path)
        assert loaded.swarm_name == "Save Test"
        assert "agent-1" in loaded.agents
        assert loaded.agents["agent-1"].role == "Test Agent"

    def test_to_dict(self, sample_config):
        """Test converting config to dictionary."""
        data = sample_config.to_dict()
        assert data["swarm_name"] == "Test Swarm"
        assert "agents" in data
        assert "agent-1" in data["agents"]
        assert data["agents"]["agent-1"]["role"] == "Test Agent 1"

    def test_get_config_path(self, temp_dir):
        """Test getting config path."""
        config = Config(swarm_dir=temp_dir)
        path = config.get_config_path()
        assert path == os.path.join(temp_dir, "swarm-config.json")
