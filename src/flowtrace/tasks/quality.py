import pandas as pd
import pandera.pandas as pa
from prefect import task

# Quality Gate Schema
# Checks logical boundaries and null values. A failure here halts the pipeline natively.
quality_schema = pa.DataFrameSchema(
    {
        "age": pa.Column(int, checks=[pa.Check.ge(0), pa.Check.le(120)], nullable=False),
        "income": pa.Column(float, checks=pa.Check.ge(0.0), nullable=False),
        "credit_score": pa.Column(int, checks=[pa.Check.ge(300), pa.Check.le(850)], nullable=False),
        "target": pa.Column(int, checks=pa.Check.isin([0, 1]), nullable=False),
    }
)


@task(name="Data Quality Gate")
def validate_quality(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies rigorous data-quality constraints.
    Halts the DAG automatically if validation fails via Pandera SchemaError.
    """
    df_clean = quality_schema.validate(df)
    return df_clean
