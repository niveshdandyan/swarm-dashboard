# Contributing to Swarm Dashboard

Thank you for your interest in contributing to Swarm Dashboard!

## Development Setup

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/swarm-dashboard.git
   cd swarm-dashboard
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Code Style

This project uses:
- **ruff** for linting and formatting
- **mypy** for type checking
- **pytest** for testing

Run checks locally:
```bash
ruff check src tests
ruff format src tests
mypy src
pytest tests -v
```

## Pull Request Process

1. Create a feature branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes with clear, descriptive commits

3. Add tests for new functionality

4. Update documentation as needed

5. Run all checks:
   ```bash
   ruff check src tests
   mypy src
   pytest tests
   ```

6. Push and open a pull request

## Commit Messages

Use clear, descriptive commit messages:
- `feat: Add new feature`
- `fix: Fix bug in X`
- `docs: Update documentation`
- `test: Add tests for X`
- `refactor: Refactor X for clarity`

## Testing

- Write tests for new features
- Ensure all tests pass before submitting
- Aim for good test coverage

## Questions?

Open an issue for questions or discussion.
