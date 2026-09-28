import mlflow
from flowtrace.config import MLFLOW_TRACKING_URI
from prefect import task
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score


@task(name="Train Model")
def train_model(features: dict, data_version: str) -> tuple[RandomForestClassifier, str, dict]:
    """
    Trains the model, logs to MLflow, and establishes the lineage record.
    """
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    X_train = features["X_train"]
    y_train = features["y_train"]
    X_test = features["X_test"]
    y_test = features["y_test"]

    # Parameterization
    n_estimators = 100
    max_depth = 5

    # Start MLflow explicit tracking (context tied to Prefect run)
    with mlflow.start_run() as run:
        model = RandomForestClassifier(
            n_estimators=n_estimators, max_depth=max_depth, random_state=42
        )
        model.fit(X_train, y_train)

        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        f1 = f1_score(y_test, preds)

        # Lineage & parameter tracking
        mlflow.log_param("data_hash", data_version)
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)

        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1_score", f1)

        # Log model artifact
        mlflow.sklearn.log_model(model, "model")

        metrics = {"accuracy": acc, "f1_score": f1}

    return model, run.info.run_id, metrics
