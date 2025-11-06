import numpy as np


def numeric_mean_diff_score(ref_series, cur_series):
    """A simple normalized mean-difference score (like z): |mean1-mean2| / pooled_std
    Returns float; higher means more drift.
    """
    a = np.array(ref_series.dropna())
    b = np.array(cur_series.dropna())
    if a.size == 0 or b.size == 0:
        return None
    mean_diff = abs(a.mean() - b.mean())
    pooled_std = np.sqrt(((a.std(ddof=1) ** 2) + (b.std(ddof=1) ** 2)) / 2.0)
    if pooled_std == 0:
        return 0.0
    return float(mean_diff / pooled_std)


def run_drift(reference_df, current_df):
    """Compute drift scores for numeric columns and return a dict.
    Uses numeric_mean_diff_score per column.
    """
    numeric_cols = reference_df.select_dtypes(include=["number"]).columns.intersection(
        current_df.select_dtypes(include=["number"]).columns
    )
    scores = {}
    for col in numeric_cols:
        scores[col] = numeric_mean_diff_score(reference_df[col], current_df[col])
    # summarize
    numeric_scores = [v for v in scores.values() if v is not None]
    summary = {"max": max(numeric_scores) if numeric_scores else None, "per_column": scores}
    return summary
