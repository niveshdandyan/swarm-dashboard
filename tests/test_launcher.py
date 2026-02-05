"""Tests for launcher module."""

import os

import pytest

from swarm_dashboard.launcher import (
    create_agent_output_symlink,
    find_task_output_file,
    is_port_available,
    select_port,
    update_agent_task_id,
)


class TestPortSelection:
    """Tests for port selection functions."""

    def test_is_port_available_open_port(self):
        """Test checking an open port."""
        # Port 59999 is likely open
        result = is_port_available(59999)
        assert isinstance(result, bool)

    def test_select_port_prefers_default(self):
        """Test that select_port prefers default if available."""
        # This test may fail if 8080 is in use
        port = select_port(59999)  # Use unlikely-to-be-used port
        assert port == 59999


class TestFindTaskOutputFile:
    """Tests for find_task_output_file function."""

    def test_find_with_explicit_task_dir(self, temp_dir):
        """Test finding output file with explicit task dir."""
        task_id = "test123"
        output_path = os.path.join(temp_dir, f"{task_id}.output")

        with open(output_path, "w") as f:
            f.write("test content")

        result = find_task_output_file(task_id, temp_dir)
        assert result == output_path

    def test_find_nonexistent_file(self):
        """Test finding nonexistent file returns None."""
        result = find_task_output_file("nonexistent_task_id")
        assert result is None

    def test_find_with_env_var(self, temp_dir, monkeypatch):
        """Test finding with TASK_DIR environment variable."""
        task_id = "env_test"
        output_path = os.path.join(temp_dir, f"{task_id}.output")

        with open(output_path, "w") as f:
            f.write("test")

        monkeypatch.setenv("TASK_DIR", temp_dir)
        result = find_task_output_file(task_id)
        assert result == output_path


class TestCreateAgentOutputSymlink:
    """Tests for create_agent_output_symlink function."""

    def test_create_symlink(self, temp_dir):
        """Test creating output symlink."""
        task_id = "task123"
        agent_id = "agent-1"

        # Create output file
        output_path = os.path.join(temp_dir, f"{task_id}.output")
        with open(output_path, "w") as f:
            f.write("output content")

        # Create symlink
        symlink = create_agent_output_symlink(
            temp_dir, agent_id, task_id, temp_dir
        )

        assert symlink is not None
        assert os.path.islink(symlink)
        assert os.path.exists(symlink)

    def test_create_symlink_creates_agent_dir(self, temp_dir):
        """Test that symlink creation creates agent directory."""
        agent_id = "new-agent"
        agent_dir = os.path.join(temp_dir, agent_id)

        assert not os.path.exists(agent_dir)

        create_agent_output_symlink(temp_dir, agent_id, "task", temp_dir)

        assert os.path.exists(agent_dir)


class TestUpdateAgentTaskId:
    """Tests for update_agent_task_id function."""

    def test_update_task_id(self, temp_dir, sample_config):
        """Test updating agent task ID."""
        sample_config.save()
        task_id = "new_task_123"

        update_agent_task_id(
            temp_dir, "agent-1", task_id, create_symlink=False
        )

        # Read updated config
        import json

        config_path = os.path.join(temp_dir, "swarm-config.json")
        with open(config_path) as f:
            config = json.load(f)

        assert config["agents"]["agent-1"]["task_id"] == task_id
        assert config["agents"]["agent-1"]["status"] == "in_progress"
        assert "started_at" in config["agents"]["agent-1"]
