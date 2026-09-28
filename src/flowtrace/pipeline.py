import mlflow
from prefect import flow

from flowtrace.config import DATA_FILE_PATH, MLFLOW_EXPERIMENT_NAME, MLFLOW_TRACKING_URI
from flowtrace.tasks.evaluate import evaluate_and_publish
from flowtrace.tasks.features import engineer_features
from flowtrace.tasks.ingest import ingest_data
from flowtrace.tasks.quality import validate_quality
from flowtrace.tasks.train import train_model


@flow(name="FlowTrace-Training-DAG", log_prints=True)
def training_pipeline():
    """
    Main explicit DAG orchestrating the pipeline stages.
    """
    # Configure global MLflow backend
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)

    print(f"Starting FlowTrace ML Pipeline. Data Target: {DATA_FILE_PATH}")

    # Stage 1: Ingestion (Schema Check) & Fingerprinting
    raw_data, data_hash = ingest_data(DATA_FILE_PATH)
    print(f"Data footprint established: {data_hash}")

    # Stage 2: Strict Quality Gate (Halts run if violation occurs)
    clean_data = validate_quality(raw_data)
    print("Quality gate passed successfully.")

    # Stage 3: Feature Engineering
    features = engineer_features(clean_data)

    # Stage 4: Model Training (Consumes Features, outputs lineage records)
    model, run_id, metrics = train_model(features, data_hash)
    print(f"Model trained successfully. Run ID: {run_id}, Metrics: {metrics}")

    # Stage 5: Evaluation vs Current Production
    evaluate_and_publish(run_id, metrics)
    print("Pipeline execution completed successfully.")
