from typing import List

import numpy as np
import pandas as pd


def rolling_mean(series: pd.Series, window: int) -> List[float]:
    result = []
    values = series.tolist()  # Use tolist() to match original behavior for type errors

    # Handle window = 0 case to match original behavior (ZeroDivisionError)
    if window == 0:
        # Simulate the original loop that would cause division by zero
        for i in range(len(values)):
            if i >= window - 1:  # This will be i >= -1, so always true for i >= 0
                # This will cause division by zero like the original
                window_sum = 0
                for j in range(window):  # range(0) is empty, so window_sum stays 0
                    window_sum += values[i - j]
                result.append(window_sum / window)  # Division by zero here
            else:
                result.append(np.nan)
        return result

    # For negative windows, continue with optimized logic but handle edge cases
    if window < 0:
        # Use the original slow logic to match behavior exactly
        for i in range(len(values)):
            if i < window - 1:
                result.append(np.nan)
            else:
                window_sum = 0
                for j in range(window):
                    window_sum += values[i - j]
                result.append(window_sum / window)
        return result

    # Optimized path for positive windows
    n = len(values)
    if window > n:
        # If window is larger than series, all values should be NaN
        return [np.nan] * n

    # Convert to numpy array for optimization, but handle type errors
    try:
        values_array = np.array(values, dtype=float)
    except (ValueError, TypeError):
        # Fall back to original logic if conversion fails
        for i in range(len(values)):
            if i < window - 1:
                result.append(np.nan)
            else:
                window_sum = 0
                for j in range(window):
                    window_sum += values[i - j]
                result.append(window_sum / window)
        return result

    # Pre-allocate result array with NaN
    result_array = np.full(n, np.nan, dtype=float)

    # Compute the cumulative sum for fast window summing
    cumsum = np.cumsum(values_array, dtype=float)
    # The sum of the first 'window' values is cumsum[window-1]
    result_array[window - 1] = cumsum[window - 1] / window
    for i in range(window, n):
        result_array[i] = (cumsum[i] - cumsum[i - window]) / window

    return result_array.tolist()
