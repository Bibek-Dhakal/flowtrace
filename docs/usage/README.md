# Usage & Operations Guide

This guide details how to interact with the FlowTrace pipeline and configure its parameters.

## Configuration & Environment Variables

FlowTrace utilizes standard environment variables. You can provide these directly or via a `.env` file in the root
directory.

| Variable                 | Type   | Default Value         | Description                                      |
|--------------------------|--------|-----------------------|--------------------------------------------------|
| `MLFLOW_TRACKING_URI`    | String | `sqlite:///mlruns.db` | Target URI for MLflow experiment tracking.       |
| `MLFLOW_EXPERIMENT_NAME` | String | `flowtrace_pipeline`  | Identifier grouping all runs in MLflow.          |
| `DATA_FILE_PATH`         | String | `data/raw_data.csv`   | Relative or absolute path to the input CSV data. |

## Running the Pipeline

Execute the primary Prefect flow:

```bash
python -m flowtrace.main
```

If the execution is successful, Prefect will output the final status of the DAG and MLflow will have securely registered
your artifacts.

## Viewing the UI (Lineage & Registry)

Launch the safe local UI wrapper (forces a single worker to prevent multiprocessing errors on Windows):

```bash
python -m flowtrace.ui
```

This will open the MLflow server locally at `http://127.0.0.1:5000`. From here, you can inspect run parameters, model
metrics, and view registered aliases (e.g., `@champion`).
