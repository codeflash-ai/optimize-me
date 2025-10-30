import numpy as np


def gradient_descent(
    X: np.ndarray, y: np.ndarray, learning_rate: float = 0.01, iterations: int = 1000
) -> np.ndarray:
    m, n = X.shape
    weights = np.zeros(n)
    for _ in range(iterations):
        predictions = np.zeros(m)
        for i in range(m):
            for j in range(n):
                predictions[i] += X[i, j] * weights[j]
        errors = predictions - y
        gradient = np.zeros(n)
        for j in range(n):
            for i in range(m):
                gradient[j] += errors[i] * X[i, j]
            gradient[j] /= m
        for j in range(n):
            weights[j] -= learning_rate * gradient[j]
    return weights
