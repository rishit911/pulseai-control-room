import pandas as pd
from sklearn.metrics import accuracy_score


def demographic_parity_disparity(df, sensitive_col, prediction_col):
    """Compute disparity of positive prediction rates across sensitive groups."""
    rates = df.groupby(sensitive_col)[prediction_col].mean()
    return float(rates.max() - rates.min()), rates.to_dict()


def run_fairness(reference_df, current_df, sensitive_col, prediction_col, label_col=None):
    """Return fairness metrics computed on the current_df and a small summary."""
    res = {}
    disparity, per_group = demographic_parity_disparity(current_df, sensitive_col, prediction_col)
    res["disparity"] = disparity
    res["per_group_positive_rate"] = per_group
    if label_col is not None and label_col in current_df.columns:
        res["accuracy"] = accuracy_score(current_df[label_col], current_df[prediction_col])
    return res
