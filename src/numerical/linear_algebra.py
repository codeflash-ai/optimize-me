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


def naive_matrix_determinant(matrix: List[List[float]]) -> float:
    """Calculate determinant using cofactor expansion."""
    n = len(matrix)

    if n == 1:
        return matrix[0][0]

    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    determinant = 0
    for j in range(n):
        # Create submatrix by removing first row and column j
        submatrix = []
        for i in range(1, n):
            row = []
            for k in range(n):
                if k != j:
                    row.append(matrix[i][k])
            submatrix.append(row)

        sign = (-1) ** j
        determinant += sign * matrix[0][j] * naive_matrix_determinant(submatrix)

    return determinant


def slow_matrix_inverse(matrix: List[List[float]]) -> List[List[float]]:
    """Calculate matrix inverse using cofactor method."""
    n = len(matrix)
    determinant = naive_matrix_determinant(matrix)

    if abs(determinant) < 1e-10:
        raise ValueError("Matrix is singular, cannot be inverted")

    # Calculate cofactor matrix
    cofactors = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            # Create submatrix by removing row i and column j
            submatrix = []
            for r in range(n):
                if r != i:
                    row = []
                    for c in range(n):
                        if c != j:
                            row.append(matrix[r][c])
                    submatrix.append(row)

            sign = (-1) ** (i + j)
            cofactors[i][j] = sign * naive_matrix_determinant(submatrix)

    # Transpose cofactor matrix
    adjoint = [[cofactors[j][i] for j in range(n)] for i in range(n)]

    # Divide by determinant
    inverse = [[adjoint[i][j] / determinant for j in range(n)] for i in range(n)]

    return inverse


def linear_equation_solver(A: List[List[float]], b: List[float]) -> List[float]:
    """Solve system of linear equations Ax = b using Gaussian elimination."""
    n = len(A)

    # Create augmented matrix [A|b]
    augmented = [row[:] + [b[i]] for i, row in enumerate(A)]

    # Forward elimination
    for i in range(n):
        # Find pivot
        max_idx = i
        for j in range(i + 1, n):
            if abs(augmented[j][i]) > abs(augmented[max_idx][i]):
                max_idx = j

        # Swap rows
        augmented[i], augmented[max_idx] = augmented[max_idx], augmented[i]

        # Eliminate below
        for j in range(i + 1, n):
            factor = augmented[j][i] / augmented[i][i]
            for k in range(i, n + 1):
                augmented[j][k] -= factor * augmented[i][k]

    # Back substitution
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = augmented[i][n]
        for j in range(i + 1, n):
            x[i] -= augmented[i][j] * x[j]
        x[i] /= augmented[i][i]

    return x
