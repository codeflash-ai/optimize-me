from typing import List, Tuple

import numpy as np


def numpy_matmul(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    rows_A, cols_A = A.shape
    rows_B, cols_B = B.shape
    if cols_A != rows_B:
        raise ValueError("Incompatible matrices")
    result = np.zeros((rows_A, cols_B))
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i, j] += A[i, k] * B[k, j]
    return result


def dot_product(a: np.ndarray, b: np.ndarray) -> float:
    if len(a) != len(b):
        raise ValueError("Vectors must have the same length")
    result = 0
    for i in range(len(a)):
        result += a[i] * b[i]
    return result


def matrix_inverse(matrix: np.ndarray) -> np.ndarray:
    if matrix.shape[0] != matrix.shape[1]:
        raise ValueError("Matrix must be square")
    n = matrix.shape[0]
    identity = np.eye(n)
    augmented = np.hstack((matrix, identity))
    for i in range(n):
        pivot = augmented[i, i]
        augmented[i] = augmented[i] / pivot
        for j in range(n):
            if i != j:
                factor = augmented[j, i]
                augmented[j] = augmented[j] - factor * augmented[i]
    return augmented[:, n:]


def matrix_multiply(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    if not A or not B or len(A[0]) != len(B):
        raise ValueError("Invalid matrix dimensions for multiplication")
    rows_A = len(A)
    cols_A = len(A[0])
    cols_B = len(B[0])
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result


def matrix_decomposition_LU(A: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    n = A.shape[0]
    L = np.zeros((n, n))
    U = np.zeros((n, n))
    for i in range(n):
        for k in range(i, n):
            sum_val = 0
            for j in range(i):
                sum_val += L[i, j] * U[j, k]
            U[i, k] = A[i, k] - sum_val
        L[i, i] = 1
        for k in range(i + 1, n):
            sum_val = 0
            for j in range(i):
                sum_val += L[k, j] * U[j, i]
            if U[i, i] == 0:
                raise ValueError("Cannot perform LU decomposition")
            L[k, i] = (A[k, i] - sum_val) / U[i, i]
    return L, U
