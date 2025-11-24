import numpy as np


def gradient_descent(
    X: np.ndarray, y: np.ndarray, learning_rate: float = 0.01, iterations: int = 1000
) -> np.ndarray:
    m, n = X.shape
    weights = np.zeros(n)
    for _ in range(iterations):
        predictions = X.dot(weights)
        errors = predictions - y
        gradient = X.T.dot(errors) / m
        weights -= learning_rate * gradient
    return weights
