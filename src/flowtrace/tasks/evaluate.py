import mlflow
from flowtrace.config import MLFLOW_TRACKING_URI
from mlflow.tracking import MlflowClient
from prefect import task


@task(name="Evaluate vs Production")
def evaluate_and_publish(run_id: str, new_metrics: dict, model_name: str = "FlowTraceClassifier"):
    """
    Compares the newly trained model against the currently registered 'Production' model.
    Registers and transitions the new model if it is an improvement or if no Prod model exists.
    """
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    client = MlflowClient()

    # 1. Register the newly trained model from this run
    model_uri = f"runs:/{run_id}/model"
    new_model_version = mlflow.register_model(model_uri, model_name)

    try:
        # Find the latest Production model
        latest_prod = client.get_latest_versions(model_name, stages=["Production"])
        if not latest_prod:
            promote = True
        else:
            prod_version = latest_prod[0]
            prod_run_id = prod_version.run_id
            prod_metrics = client.get_run(prod_run_id).data.metrics

            # 2. Gate Comparison
            new_f1 = new_metrics.get("f1_score", 0)
            prod_f1 = prod_metrics.get("f1_score", 0)

            print(f"Performance check -> New F1: {new_f1:.4f} | Prod F1: {prod_f1:.4f}")
            promote = new_f1 >= prod_f1

    except Exception as e:
        print(f"No existing production models found or error retrieving them: {e}")
        promote = True

    # 3. Publish Decision
    if promote:
        print(f"Promoting model version {new_model_version.version} to Production.")
        client.transition_model_version_stage(
            name=model_name,
            version=new_model_version.version,
            stage="Production",
            archive_existing_versions=True,
        )
    else:
        print(
            f"New model version {new_model_version.version} did not outperform Production. "
            f"Keeping current model."
        )
