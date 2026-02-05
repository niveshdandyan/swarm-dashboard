"""Pytest configuration and fixtures."""

import json
import os
import tempfile
from typing import Generator

import pytest

from swarm_dashboard.config import AgentConfig, Config


@pytest.fixture
def temp_dir() -> Generator[str, None, None]:
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sample_config(temp_dir: str) -> Config:
    """Create a sample configuration."""
    config = Config(
        swarm_name="Test Swarm",
        swarm_dir=temp_dir,
        task_dir=temp_dir,
        port=8080,
        start_time="2024-01-01T00:00:00Z",
    )
    config.agents = {
        "agent-1": AgentConfig(
            role="Test Agent 1",
            wave=1,
            mission="Test mission 1",
        ),
        "agent-2": AgentConfig(
            role="Test Agent 2",
            wave=2,
            mission="Test mission 2",
        ),
    }
    return config


@pytest.fixture
def config_file(temp_dir: str, sample_config: Config) -> str:
    """Create a config file in the temp directory."""
    config_path = sample_config.save()
    return config_path


@pytest.fixture
def sample_jsonl_content() -> str:
    """Sample JSONL content for testing."""
    events = [
        {"type": "assistant", "name": "Read", "content": "Reading file"},
        {"type": "tool_result", "name": "Read", "content": "File content"},
        {"type": "assistant", "name": "Write", "input": {"file_path": "/test/file.py"}},
        {"type": "tool_result", "name": "Write", "content": "File written"},
        {"name": "Bash", "input": {"command": "ls -la"}},
    ]
    return "\n".join(json.dumps(e) for e in events)


@pytest.fixture
def output_file(temp_dir: str, sample_jsonl_content: str) -> str:
    """Create a sample output file."""
    output_path = os.path.join(temp_dir, "test.output")
    with open(output_path, "w") as f:
        f.write(sample_jsonl_content)
    return output_path
