import hashlib

import pandas as pd
import pandera.pandas as pa
from prefect import task

# Initial Ingestion Schema (Schema Validation Only)
# Ensures columns exist and types match before moving to quality checks.
ingest_schema = pa.DataFrameSchema(
    {
        "age": pa.Column(int, coerce=True),
        "income": pa.Column(float, coerce=True),
        "credit_score": pa.Column(int, coerce=True),
        "target": pa.Column(int, coerce=True),
    },
    strict=True,
)


@task(name="Ingest & Schema Validate Data")
def ingest_data(file_path: str) -> tuple[pd.DataFrame, str]:
    """
    Reads data and performs strict schema presence validation.
    Returns the dataframe and a sha256 hash of the data for lineage.
    """
    df = pd.read_csv(file_path)
    df_validated = ingest_schema.validate(df)

    # Generate data fingerprint (hash) to link model to this exact data version
    data_hash = hashlib.sha256(
        pd.util.hash_pandas_object(df_validated, index=True).values
    ).hexdigest()

    return df_validated, data_hash
