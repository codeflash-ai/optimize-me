from typing import List

import numpy as np
import pandas as pd


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
