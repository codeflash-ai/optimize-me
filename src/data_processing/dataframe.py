from typing import List, Callable, Any

import numpy as np
import pandas as pd

from src.telemetry.decorators import trace_function


@trace_function
def dataframe_filter(df: pd.DataFrame, column: str, value: Any) -> pd.DataFrame:
    indices = []
    for i in range(len(df)):
        if df.iloc[i][column] == value:
            indices.append(i)
    return df.iloc[indices].reset_index(drop=True)


@trace_function
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


@trace_function
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
