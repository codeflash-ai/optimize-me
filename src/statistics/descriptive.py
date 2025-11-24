from typing import Tuple

import numpy as np
import pandas as pd


def describe(series: pd.Series) -> dict[str, float]:
    values = [v for v in series if not pd.isna(v)]
    n = len(values)
    if n == 0:
        return {
            "count": 0,
            "mean": np.nan,
            "std": np.nan,
            "min": np.nan,
            "25%": np.nan,
            "50%": np.nan,
            "75%": np.nan,
            "max": np.nan,
        }
    sorted_values = sorted(values)
    mean = sum(values) / n
    variance = sum((x - mean) ** 2 for x in values) / n
    std = variance**0.5

    def percentile(p):
        idx = int(p * n / 100)
        if idx >= n:
            idx = n - 1
        return sorted_values[idx]

    return {
        "count": n,
        "mean": mean,
        "std": std,
        "min": sorted_values[0],
        "25%": percentile(25),
        "50%": percentile(50),
        "75%": percentile(75),
        "max": sorted_values[-1],
    }


def correlation(df: pd.DataFrame) -> dict[Tuple[str, str], float]:
    numeric_columns = [
        col for col in df.columns if np.issubdtype(df[col].dtype, np.number)
    ]
    n_cols = len(numeric_columns)
    result = {}

    # Extract numeric columns as arrays up front for efficient access
    data = {col: df[col].to_numpy() for col in numeric_columns}
    isnan = {col: np.isnan(data[col]) for col in numeric_columns}

    for i in range(n_cols):
        col_i = numeric_columns[i]
        arr_i = data[col_i]
        isnan_i = isnan[col_i]
        for j in range(n_cols):
            col_j = numeric_columns[j]
            arr_j = data[col_j]
            isnan_j = isnan[col_j]
            # Mask for rows where both values are NOT nan
            valid_mask = ~(isnan_i | isnan_j)
            if not np.any(valid_mask):
                result[(col_i, col_j)] = np.nan
                continue
            x = arr_i[valid_mask]
            y = arr_j[valid_mask]
            n = x.shape[0]
            mean_x = np.sum(x) / n
            mean_y = np.sum(y) / n
            var_x = np.sum((x - mean_x) ** 2) / n
            var_y = np.sum((y - mean_y) ** 2) / n
            std_x = var_x**0.5
            std_y = var_y**0.5
            if std_x == 0 or std_y == 0:
                result[(col_i, col_j)] = np.nan
                continue
            cov = np.sum((x - mean_x) * (y - mean_y)) / n
            corr = cov / (std_x * std_y)
            result[(col_i, col_j)] = corr
    return result
