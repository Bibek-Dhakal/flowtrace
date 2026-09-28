import pytest
from flowtrace.tasks.quality import validate_quality
from pandera.errors import SchemaError


def test_quality_gate_passes_on_valid_data(dummy_valid_dataframe):
    """Test that valid data seamlessly passes the quality gate."""
    # Since tasks return prefect State implicitly when run normally,
    # we call `.fn()` to test the underlying python code directly
    validated_df = validate_quality.fn(dummy_valid_dataframe)
    assert len(validated_df) == 3
    assert list(validated_df.columns) == ["age", "income", "credit_score", "target"]


def test_quality_gate_fails_on_out_of_bounds_data(dummy_valid_dataframe):
    """Test that data violating bounds triggers a failure."""
    bad_df = dummy_valid_dataframe.copy()
    bad_df.loc[0, "age"] = -5  # Invalid age

    with pytest.raises(SchemaError):
        validate_quality.fn(bad_df)


def test_quality_gate_fails_on_null_data(dummy_valid_dataframe):
    """Test that null data triggers a pipeline failure."""
    bad_df = dummy_valid_dataframe.copy()
    bad_df.loc[1, "income"] = None

    with pytest.raises(SchemaError):
        validate_quality.fn(bad_df)
