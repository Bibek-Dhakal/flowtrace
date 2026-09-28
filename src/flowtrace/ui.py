import os
import subprocess
import sys

from flowtrace.config import MLFLOW_TRACKING_URI


def start_ui():
    """
    Launches the MLflow tracking UI.
    Enforces a single worker to prevent Uvicorn multiprocessing socket errors on Windows.
    """
    cmd = [
        "mlflow",
        "server",
        "--backend-store-uri",
        MLFLOW_TRACKING_URI,
        "--host",
        "127.0.0.1",
        "--port",
        "5000",
        "--workers",
        "1",
    ]

    print("🌊 Starting FlowTrace MLflow UI...")
    print(f"Executing: {' '.join(cmd)}")

    # Suppress Starlette/Uvicorn Python deprecation warnings in the MLflow subprocess
    env = os.environ.copy()
    env["PYTHONWARNINGS"] = "ignore"

    try:
        subprocess.run(cmd, check=True, env=env)
    except KeyboardInterrupt:
        print("\nShutting down MLflow UI.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to start MLflow UI: {e}")
        sys.exit(1)


if __name__ == "__main__":
    start_ui()
