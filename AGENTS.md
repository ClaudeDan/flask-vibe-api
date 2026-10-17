# Project Guidelines

## Current State
- This workspace currently contains `requirements.txt` and a local `.venv/`; no Flask application, tests, README, or build/test configuration is present yet.
- Inspect the current files before assuming an application entry point, route layout, test framework, or run command.

## Dependencies and Environment
- Keep Python runtime dependencies declared in `requirements.txt`; install them with `python -m pip install -r requirements.txt` in the selected environment.
- On Windows, use the workspace virtual environment when available: `\.venv\Scripts\python.exe` (relative form: `.\.venv\Scripts\python.exe`). Do not treat `.venv/` as project source.

## Validation
- No test or lint command is defined yet. When adding application behavior, add focused automated tests and document the command that runs them; report only checks that were actually run.