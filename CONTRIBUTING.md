# Contributing Guidelines

Thank you for contributing to FlowTrace!

## Code Standards
- This project strictly enforces **Conventional Commits** (`feat:`, `fix:`, `chore:`, etc.). Your PR titles and commits must follow this format to enable automated versioning.
- Ensure your code passes all linting and formatting checks. We use `Ruff` for Python code quality.

## Automated Versioning
We use Google's `release-please` via GitHub Actions for automated versioning and `CHANGELOG.md` generation. 
- A Release PR will automatically aggregate your changes based on your commit prefixes.
- Never manually increment version numbers in `pyproject.toml`; the Release PR handles this upon merging.

## Submitting a PR
1. Create a feature branch.
2. Commit your changes using Conventional Commits.
3. Push to your fork and submit a Pull Request.
4. Ensure all CI checks (pytest, pre-commit) pass before requesting a review.