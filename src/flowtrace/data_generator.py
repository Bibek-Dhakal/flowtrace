import os

import numpy as np
import pandas as pd

from flowtrace.config import DATA_FILE_PATH


def generate_dummy_data():
    """Generates a synthetic dataset for testing the pipeline."""
    os.makedirs(os.path.dirname(DATA_FILE_PATH), exist_ok=True)

    np.random.seed(42)
    n_samples = 500

    data = {
        "age": np.random.randint(18, 80, n_samples),
        "income": np.random.normal(50000, 15000, n_samples),
        "credit_score": np.random.randint(300, 850, n_samples),
        "target": np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
    }

    df = pd.DataFrame(data)
    df.to_csv(DATA_FILE_PATH, index=False)
    print(f"✅ Generated {n_samples} rows of synthetic data at {DATA_FILE_PATH}")


if __name__ == "__main__":
    generate_dummy_data()
