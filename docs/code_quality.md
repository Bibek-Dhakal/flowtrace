# Code Quality Standard

Automated quality checks run locally on `git commit` via pre-commit hooks and ensure uniformity across the codebase.

## Environment Setup

To register and activate the hooks locally:

```bash
# Install pre-commit (if not already installed via pip)
pip install pre-commit

# Install hooks into your local git repository
pre-commit install
pre-commit install --hook-type commit-msg
```

## Manual Execution Commands

Run repository-wide on ALL files:

```bash
pre-commit run --all-files
```

Run checks ONLY on staged files (default behavior on commit):

```bash
pre-commit run
```

Run individual tools directly:

```bash
# Python Formatting & Linting
ruff check src/
ruff format src/
```

## Emergency Bypassing

If you urgently need to bypass formatting/linting for a hotfix (use responsibly):

```bash
git commit -m "fix: emergency hotfix" --no-verify
```

*Note: We highly recommend resolving all quality issues as CI pipelines will enforce them regardless.*