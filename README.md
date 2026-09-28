# FlowTrace 🌊

DAG-orchestrated, parameterized, lineage-tracked ML pipeline.

FlowTrace is built to demonstrate mid-level machine learning engineering capabilities. It closes the gap between
standard Jupyter notebook scripts and production-ready ML engineering by utilizing an explicit DAG, strict data quality
gating, and end-to-end lineage tracking.

## Core Features

- **Orchestration**: Pipeline orchestrated as a Direct Acyclic Graph (DAG) using `Prefect`.
- **Quality Gates**: Invalid or degraded data halts the pipeline immediately using `pandera`.
- **Lineage**: Every model artifact is linked to the exact data version (hash) and run ID via `MLflow`.
- **Automated Evaluation**: Newly trained models are evaluated against the latest production model and automatically
  gated based on relative performance.

## Documentation Navigation

- [Value Proposition & Tech Benefits](docs/value_proposition.md) 🌟 Start Here
- [Usage Guide](docs/usage/README.md)
- [Architecture & Design](docs/architecture/README.md)
- [Code Quality & Linting](docs/code_quality.md)
- [Testing Standards](docs/testing/README.md)

## Quick Start

1. **Install**:
   ```bash
   pip install -e ".[dev,test]"
   ```
2. **Setup Tools**:
   ```bash
   pre-commit install
   ```
3. **Generate Dummy Data**:
   ```bash
   python -m flowtrace.data_generator
   ```
4. **Run the Pipeline**:
   ```bash
   python -m flowtrace.main
   ```
5. **View Lineage & UI**:
   ```bash
   python -m flowtrace.ui
   ```
   