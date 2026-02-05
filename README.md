# Swarm Dashboard

[![CI](https://github.com/niveshdandyan/swarm-dashboard/actions/workflows/ci.yml/badge.svg)](https://github.com/niveshdandyan/swarm-dashboard/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/swarm-dashboard.svg)](https://badge.fury.io/py/swarm-dashboard)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Live real-time dashboard for monitoring AI agent swarms with smart completion detection, clickable agent detail views, and activity streaming.

```
+-----------------------------------------------------------------+
|                    SWARM DASHBOARD v6                           |
|            "See your agents work in real-time"                  |
+-----------------------------------------------------------------+
|  Agent 1 [####################] 100% COMPLETED  (5m ago)        |
|  Agent 2 [##########..........]  50% Running... (2s ago)        |
|  Agent 3 [########............]  40% IDLE       (90s ago)       |
|  Agent 4 [....................]   0% Pending                    |
+-----------------------------------------------------------------+
```

## Features

- **Real-time Updates** - Auto-refreshes every 2 seconds without page reload
- **Smart Completion Detection** - Auto-detects when agents finish
- **Beautiful UI** - Capybara-inspired natural color palette with light/dark themes
- **Clickable Agent Details** - See live activity feed, tools used, files created
- **Zero Dependencies** - Pure Python stdlib + vanilla HTML/CSS/JS
- **Type Annotated** - Full type hints for IDE support

## Installation

### From PyPI

```bash
pip install swarm-dashboard
```

### From Source

```bash
git clone https://github.com/niveshdandyan/swarm-dashboard.git
cd swarm-dashboard
pip install -e .
```

### As a Claude Code Skill

```bash
git clone https://github.com/niveshdandyan/swarm-dashboard.git ~/.claude/skills/swarm-dashboard
```

## Quick Start

### Command Line

```bash
# Start server with environment variables
export SWARM_DIR="/workspace/my-project"
export SWARM_NAME="My Project Swarm"
swarm-dashboard serve

# Or with CLI arguments
swarm-dashboard serve --port 8080 --swarm-dir /workspace/my-project

# Launch in background
swarm-dashboard launch --name "My Swarm" --dir /workspace/my-project

# Check status
swarm-dashboard status --dir /workspace/my-project

# Stop dashboard
swarm-dashboard stop --dir /workspace/my-project
```

### Python API

```python
from swarm_dashboard import launch_dashboard, update_agent_task_id

# Launch dashboard
url = launch_dashboard(
    swarm_name="My Project",
    swarm_dir="/workspace/my-project",
    agents={
        "agent-1": {"role": "Core Architect", "wave": 1, "mission": "Setup project"},
        "agent-2": {"role": "Backend Dev", "wave": 2, "mission": "Build API"},
    }
)
print(f"Dashboard: {url}")

# After launching agents, update their task IDs for live tracking
update_agent_task_id(
    swarm_dir="/workspace/my-project",
    agent_id="agent-1",
    task_id="abc123"  # From Claude Code Task tool
)
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SWARM_DIR` | Current directory | Directory containing agent folders |
| `TASK_DIR` | `/tmp/claude-1000` | Directory containing task output files |
| `DASHBOARD_PORT` | `8080` | HTTP server port |
| `SWARM_NAME` | `Agent Swarm` | Display name for the swarm |

### swarm-config.json

```json
{
  "swarm_name": "My Project Swarm",
  "start_time": "2024-01-01T00:00:00Z",
  "swarm_dir": "/workspace/my-project",
  "task_dir": "/tmp/claude-tasks",
  "agents": {
    "agent-1": {
      "role": "Core Architect",
      "wave": 1,
      "task_id": "abc123",
      "mission": "Set up project structure"
    }
  }
}
```

## Project Structure

```
swarm-dashboard/
├── src/swarm_dashboard/
│   ├── __init__.py       # Package exports
│   ├── __main__.py       # Module entry point
│   ├── cli.py            # CLI interface
│   ├── config.py         # Configuration management
│   ├── server.py         # HTTP server
│   ├── agents.py         # Agent status tracking
│   ├── parser.py         # JSONL parsing
│   ├── tracker.py        # File position tracking
│   ├── launcher.py       # Dashboard launcher
│   └── templates/        # HTML/CSS/JS templates
│       ├── css.py
│       ├── html.py
│       └── js.py
├── tests/                # Unit tests
├── docs/                 # Documentation
├── examples/             # Example usage
├── pyproject.toml        # Modern Python packaging
└── README.md
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Dashboard HTML page |
| `GET /api/status` | Swarm status JSON |
| `GET /api/agent/{id}` | Agent details JSON |
| `GET /health` | Health check |

## Development

```bash
# Clone repository
git clone https://github.com/niveshdandyan/swarm-dashboard.git
cd swarm-dashboard

# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests -v

# Run linter
ruff check src tests

# Run type checker
mypy src

# Install pre-commit hooks
pre-commit install
```

## License

MIT License - see [LICENSE](LICENSE) file.

## Credits

Built by AI agent swarms, for AI agent swarms.

*"Agents building the dashboard that monitors agents."*
