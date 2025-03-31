from typing import List, Tuple

import numpy as np
import pandas as pd
from typing import Callable, Any


def dataframe_filter(df: pd.DataFrame, column: str, value: Any) -> pd.DataFrame:
    indices = []
    for i in range(len(df)):
        if df.iloc[i][column] == value:
            indices.append(i)
    return df.iloc[indices].reset_index(drop=True)


def groupby_mean(df: pd.DataFrame, group_col: str, value_col: str) -> dict[Any, float]:
    sums = {}
    counts = {}
    for i in range(len(df)):
        group = df.iloc[i][group_col]
        value = df.iloc[i][value_col]
        if group in sums:
            sums[group] += value
            counts[group] += 1
        else:
            sums[group] = value
            counts[group] = 1
    result = {}
    for group in sums:
        result[group] = sums[group] / counts[group]
    return result


def dataframe_merge(
    left: pd.DataFrame, right: pd.DataFrame, left_on: str, right_on: str
) -> pd.DataFrame:
    result_data = []
    left_cols = list(left.columns)
    right_cols = [col for col in right.columns if col != right_on]
    right_dict = {}
    for i in range(len(right)):
        key = right.iloc[i][right_on]
        if key not in right_dict:
            right_dict[key] = []
        right_dict[key].append(i)
    for i in range(len(left)):
        left_row = left.iloc[i]
        key = left_row[left_on]
        if key in right_dict:
            for right_idx in right_dict[key]:
                right_row = right.iloc[right_idx]
                new_row = {}
                for col in left_cols:
                    new_row[col] = left_row[col]
                for col in right_cols:
                    new_row[col] = right_row[col]
                result_data.append(new_row)
    return pd.DataFrame(result_data)


def pivot_table(
    df: pd.DataFrame, index: str, columns: str, values: str, aggfunc: str = "mean"
) -> dict[Any, dict[Any, float]]:
    result = {}
    if aggfunc == "mean":

        def agg_func(values):
            return sum(values) / len(values)
    elif aggfunc == "sum":

        def agg_func(values):
            return sum(values)
    elif aggfunc == "count":

        def agg_func(values):
            return len(values)
    else:
        raise ValueError(f"Unsupported aggregation function: {aggfunc}")
    grouped_data = {}
    for i in range(len(df)):
        row = df.iloc[i]
        index_val = row[index]
        column_val = row[columns]
        value = row[values]
        if index_val not in grouped_data:
            grouped_data[index_val] = {}
        if column_val not in grouped_data[index_val]:
            grouped_data[index_val][column_val] = []
        grouped_data[index_val][column_val].append(value)
    for index_val in grouped_data:
        result[index_val] = {}
        for column_val in grouped_data[index_val]:
            result[index_val][column_val] = agg_func(
                grouped_data[index_val][column_val]
            )
    return result


def apply_function(df: pd.DataFrame, column: str, func: Callable) -> List[Any]:
    result = []
    for i in range(len(df)):
        value = df.iloc[i][column]
        result.append(func(value))
    return result


def fillna(df: pd.DataFrame, column: str, value: Any) -> pd.DataFrame:
    result = df.copy()
    for i in range(len(df)):
        if pd.isna(df.iloc[i][column]):
            result.iloc[i, df.columns.get_loc(column)] = value
    return result


def drop_duplicates(df: pd.DataFrame, subset: List[str] = None) -> pd.DataFrame:
    if subset is None:
        subset = df.columns.tolist()
    seen = set()
    keep_indices = []
    for i in range(len(df)):
        values = tuple(df.iloc[i][col] for col in subset)
        if values not in seen:
            seen.add(values)
            keep_indices.append(i)
    return df.iloc[keep_indices].reset_index(drop=True)


def sort_values(df: pd.DataFrame, by: str, ascending: bool = True) -> pd.DataFrame:
    indices = list(range(len(df)))
    for i in range(len(df)):
        for j in range(0, len(df) - i - 1):
            if ascending:
                condition = df.iloc[indices[j]][by] > df.iloc[indices[j + 1]][by]
            else:
                condition = df.iloc[indices[j]][by] < df.iloc[indices[j + 1]][by]
            if condition:
                indices[j], indices[j + 1] = indices[j + 1], indices[j]
    return df.iloc[indices].reset_index(drop=True)


def reindex(df: pd.DataFrame, new_index: List[Any]) -> pd.DataFrame:
    index_map = {df.index[i]: i for i in range(len(df))}
    new_data = []
    for idx in new_index:
        if idx in index_map:
            new_data.append(df.iloc[index_map[idx]])
        else:
            new_row = pd.Series({col: np.nan for col in df.columns})
            new_data.append(new_row)
    result = pd.DataFrame(new_data)
    result.index = new_index
    return result


def rolling_mean(series: pd.Series, window: int) -> List[float]:
    result = []
    values = series.tolist()
    for i in range(len(values)):
        if i < window - 1:
            result.append(np.nan)
        else:
            window_sum = 0
            for j in range(window):
                window_sum += values[i - j]
            result.append(window_sum / window)
    return result


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


def melt(df: pd.DataFrame, id_vars: List[str], value_vars: List[str]) -> pd.DataFrame:
    result_data = []
    for i in range(len(df)):
        id_values = {id_var: df.iloc[i][id_var] for id_var in id_vars}
        for value_var in value_vars:
            new_row = {
                **id_values,
                "variable": value_var,
                "value": df.iloc[i][value_var],
            }
            result_data.append(new_row)
    return pd.DataFrame(result_data)
