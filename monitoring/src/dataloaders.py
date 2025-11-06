import pandas as pd


def load_csv(path):
    """Load CSV into pandas DataFrame. Caller handles exceptions."""
    return pd.read_csv(path)
