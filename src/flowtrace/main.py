import logging
import warnings

# Suppress noisy warnings from third-party libraries (Pandera, MLflow, Starlette)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="mlflow")

# Suppress specific noisy MLflow loggers
logging.getLogger("mlflow.models.model").setLevel(logging.ERROR)
logging.getLogger("mlflow.tracking._model_registry.fluent").setLevel(logging.ERROR)

from flowtrace.pipeline import training_pipeline

if __name__ == "__main__":
    training_pipeline()
