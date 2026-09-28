import os

from dotenv import load_dotenv

load_dotenv()

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "sqlite:///mlruns.db")
MLFLOW_EXPERIMENT_NAME = os.getenv("MLFLOW_EXPERIMENT_NAME", "flowtrace_pipeline")
DATA_FILE_PATH = os.getenv("DATA_FILE_PATH", "data/raw_data.csv")
