import mlflow
from flowtrace.config import MLFLOW_TRACKING_URI
from mlflow.tracking import MlflowClient
from prefect import task


@task(name="Evaluate vs Production")
def evaluate_and_publish(run_id: str, new_metrics: dict, model_name: str = "FlowTraceClassifier"):
    """
    Compares the newly trained model against the currently registered 'champion' model.
    Registers and assigns the 'champion' alias to the new model if it is an improvement
    or if no champion model exists.
    """
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    client = MlflowClient()

    # 1. Register the newly trained model from this run
    model_uri = f"runs:/{run_id}/model"
    new_model_version = mlflow.register_model(model_uri, model_name)

    try:
        # Find the current champion model
        prod_version = client.get_model_version_by_alias(model_name, "champion")
        prod_run_id = prod_version.run_id
        prod_metrics = client.get_run(prod_run_id).data.metrics

        # 2. Gate Comparison
        new_f1 = new_metrics.get("f1_score", 0)
        prod_f1 = prod_metrics.get("f1_score", 0)

        print(f"Performance check -> New F1: {new_f1:.4f} | Champion F1: {prod_f1:.4f}")
        promote = new_f1 >= prod_f1

    except Exception as e:
        print(f"No existing champion models found or error retrieving them: {e}")
        promote = True

    # 3. Publish Decision
    if promote:
        print(f"Promoting model version {new_model_version.version} to Champion.")
        client.set_registered_model_alias(
            name=model_name,
            alias="champion",
            version=new_model_version.version,
        )
    else:
        print(
            f"New model version {new_model_version.version} did not outperform Champion. "
            f"Keeping current model."
        )
