import numpy as np


def FFT(x: np.ndarray) -> np.ndarray:
    n = len(x)
    if n == 1:
        return x
    even = FFT(x[****])
    odd = FFT(x[****])
    factor = np.exp(-2j * np.pi * np.arange(n) / n)
    result = np.zeros(n, dtype=complex)
    half_n = n // 2
    for k in range(half_n):
        result[k] = even[k] + factor[k] * odd[k]
        result[k + half_n] = even[k] - factor[k] * odd[k]
    return result
