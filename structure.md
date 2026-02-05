# Enterprise Repository Structure

```
swarm-dashboard/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml              # Lint, test, type-check
│   │   └── release.yml         # PyPI publish on tag
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       └── feature_request.md
├── src/
│   └── swarm_dashboard/
│       ├── __init__.py         # Package exports, version
│       ├── __main__.py         # CLI entry point
│       ├── server.py           # HTTP server (DashboardHandler)
│       ├── config.py           # Configuration management
│       ├── tracker.py          # FilePositionTracker, BoundedParseCache
│       ├── parser.py           # JSONL parsing, event extraction
│       ├── agents.py           # Agent status detection logic
│       ├── launcher.py         # Dashboard launcher utilities
│       ├── cli.py              # Argparse CLI interface
│       └── templates/
│           ├── __init__.py
│           ├── html.py         # HTML template string
│           ├── css.py          # CSS styles
│           └── js.py           # JavaScript code
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   ├── test_server.py
│   ├── test_config.py
│   ├── test_tracker.py
│   ├── test_parser.py
│   ├── test_agents.py
│   └── test_launcher.py
├── docs/
│   ├── index.md
│   ├── installation.md
│   ├── configuration.md
│   ├── api.md
│   └── troubleshooting.md
├── examples/
│   ├── basic_usage.py
│   ├── custom_config.py
│   └── swarm-config.example.json
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml              # Modern Python packaging
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
└── SKILL.md                    # Claude Code skill definition
```
