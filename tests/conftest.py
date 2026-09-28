import pandas as pd
import pytest


@pytest.fixture
def dummy_valid_dataframe():
    """Returns a schema-compliant dataframe for testing."""
    return pd.DataFrame(
        {
            "age": [25, 45, 60],
            "income": [50000.0, 75000.0, 120000.0],
            "credit_score": [650, 700, 800],
            "target": [0, 1, 0],
        }
    )
