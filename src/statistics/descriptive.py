from typing import Tuple

import numpy as np
import pandas as pd

from src.telemetry.decorators import trace_function


@trace_function
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


@trace_function
def correlation(df: pd.DataFrame) -> dict[Tuple[str, str], float]:
    numeric_columns = [
        col for col in df.columns if np.issubdtype(df[col].dtype, np.number)
    ]
    n_cols = len(numeric_columns)
    result = {}
    for i in range(n_cols):
        col_i = numeric_columns[i]
        for j in range(n_cols):
            col_j = numeric_columns[j]
            values_i = []
            values_j = []
            for k in range(len(df)):
                if not pd.isna(df.iloc[k][col_i]) and not pd.isna(df.iloc[k][col_j]):
                    values_i.append(df.iloc[k][col_i])
                    values_j.append(df.iloc[k][col_j])
            n = len(values_i)
            if n == 0:
                result[(col_i, col_j)] = np.nan
                continue
            mean_i = sum(values_i) / n
            mean_j = sum(values_j) / n
            var_i = sum((x - mean_i) ** 2 for x in values_i) / n
            var_j = sum((x - mean_j) ** 2 for x in values_j) / n
            std_i = var_i**0.5
            std_j = var_j**0.5
            if std_i == 0 or std_j == 0:
                result[(col_i, col_j)] = np.nan
                continue
            cov = (
                sum((values_i[k] - mean_i) * (values_j[k] - mean_j) for k in range(n))
                / n
            )
            corr = cov / (std_i * std_j)
            result[(col_i, col_j)] = corr
    return result
