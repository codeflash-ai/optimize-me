from typing import List, Any

import pandas as pd


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

    # Extract data as numpy arrays for fast iteration, avoiding .iloc row lookup
    index_data = df[index].values
    column_data = df[columns].values
    value_data = df[values].values

    for index_val, column_val, value in zip(index_data, column_data, value_data):
        inner = grouped_data.setdefault(index_val, {})
        inner.setdefault(column_val, []).append(value)

    for index_val in grouped_data:
        result[index_val] = {}
        for column_val in grouped_data[index_val]:
            result[index_val][column_val] = agg_func(
                grouped_data[index_val][column_val]
            )
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
