# Testing Strategy

Tests validate individual pipeline components (tasks) and end-to-end orchestration flow to prevent regressions in standard ML capabilities.

## Execution Procedures

Run all unit tests and integration tests:
```bash
pytest
```

Run tests with coverage reporting:
```bash
pytest --cov=src/flowtrace --cov-report=term-missing
```

## Structure
- `tests/test_pipeline.py`: Verifies that the `@task` decorators execute valid logic independently, ensuring data gating works correctly. 