# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [6.1.0] - 2024-02-05

### Added
- Enterprise-grade repository structure with modular code organization
- Full type annotations for IDE support
- Comprehensive test suite with pytest
- CI/CD pipelines with GitHub Actions
- Pre-commit hooks for code quality
- CLI commands: `serve`, `launch`, `stop`, `status`
- `pyproject.toml` for modern Python packaging
- Automatic symlink creation for live activity tracking

### Changed
- Split monolithic server into separate modules:
  - `config.py` - Configuration management
  - `server.py` - HTTP server
  - `agents.py` - Agent status tracking
  - `parser.py` - JSONL parsing
  - `tracker.py` - File position tracking
  - `launcher.py` - Dashboard launcher utilities
  - `templates/` - Separated CSS, HTML, JS
- Improved documentation with docstrings

## [6.0.0] - 2024-02-04

### Added
- Self-contained server with embedded HTML (no external file dependency)
- Line-by-line JSON parsing (replaces regex)
- FilePositionTracker for incremental file reads
- BoundedParseCache with LRU eviction (max 50 entries)
- Capybara-inspired color palette
- Instrument Serif typography for headings
- Health endpoint with version info

### Changed
- Complete UI redesign with natural color palette
- Improved memory efficiency

## [5.0.0] - 2024-02-03

### Added
- Light/dark theme toggle with localStorage persistence
- Clickable agent detail panels with slide-in animation
- Live activity feed showing real-time tool usage
- Connection status indicator with pulse animation
- Responsive design for mobile

## [3.0.0] - 2024-02-02

### Added
- Smart completion detection based on idle time and markers
- Last activity timestamp display
- Idle state detection (60-120 seconds)
- Stale activity warning

## [2.0.0] - 2024-02-01

### Added
- Clickable agent cards with detail panel
- Live activity feed
- Tool usage statistics
- Files created list

## [1.0.0] - 2024-01-31

### Added
- Initial release
- Basic status monitoring
- Progress bars and status badges
- Wave visualization
