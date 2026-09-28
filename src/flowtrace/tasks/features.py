import pandas as pd
from prefect import task
from sklearn.model_selection import train_test_split


@task(name="Feature Engineering")
def engineer_features(df: pd.DataFrame) -> dict:
    """
    Parameterized feature engineering stage.
    Splits data into train and test sets for evaluation.
    """
    X = df.drop(columns=["target"])
    y = df["target"]

    # Feature 1: Income per Age (dummy engineered feature)
    X["income_per_age"] = X["income"] / (X["age"] + 1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
    }
