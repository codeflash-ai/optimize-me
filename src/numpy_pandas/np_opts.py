from typing import List, Tuple

import math
from typing import Callable
import random


def binomial_coefficient_recursive(n: int, k: int) -> int:
    """Calculate binomial coefficient using recursive formula."""
    if k == 0 or k == n:
        return 1
    return binomial_coefficient_recursive(
        n - 1, k - 1
    ) + binomial_coefficient_recursive(n - 1, k)


def naive_matrix_determinant(matrix: List[List[float]]) -> float:
    """Calculate determinant using cofactor expansion."""

    n = len(matrix)

    if n == 1:
        return matrix[0][0]

    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    determinant = 0
    # Only create submatrices with fast list comprehension
    for j in range(n):
        # Submatrix: remove row 0, and column j
        submatrix = [row[:j] + row[j + 1 :] for row in matrix[1:]]
        # Alternate sign using bit operation for speed
        sign = -1 if (j & 1) else 1
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


def monte_carlo_pi(num_samples: int) -> float:
    """Estimate π using Monte Carlo method."""
    inside_circle = 0

    for _ in range(num_samples):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)

        if x**2 + y**2 <= 1:
            inside_circle += 1

    return 4 * inside_circle / num_samples


def sieve_of_eratosthenes(n: int) -> List[int]:
    """Find all primes up to n using sieve of Eratosthenes."""
    if n <= 1:
        return []

    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(math.sqrt(n)) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False

    return [i for i in range(2, n + 1) if is_prime[i]]


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


def newton_raphson_sqrt(x: float, epsilon: float = 1e-10, max_iter: int = 100) -> float:
    """Calculate square root using Newton-Raphson method."""
    if x < 0:
        raise ValueError("Cannot compute square root of negative number")

    if x == 0:
        return 0

    guess = x / 2  # Initial guess

    for _ in range(max_iter):
        next_guess = 0.5 * (guess + x / guess)
        if abs(next_guess - guess) < epsilon:
            return next_guess
        guess = next_guess

    return guess


def lagrange_interpolation(points: List[Tuple[float, float]], x: float) -> float:
    """Interpolate a function value using Lagrange polynomials."""
    result = 0.0
    n = len(points)

    for i in range(n):
        term = points[i][1]
        for j in range(n):
            if i != j:
                term *= (x - points[j][0]) / (points[i][0] - points[j][0])
        result += term

    return result


def bisection_method(
    f: Callable[[float], float],
    a: float,
    b: float,
    epsilon: float = 1e-10,
    max_iter: int = 100,
) -> float:
    """Find a root of function f using bisection method."""
    if f(a) * f(b) > 0:
        raise ValueError("Function must have opposite signs at endpoints")

    for _ in range(max_iter):
        c = (a + b) / 2
        fc = f(c)

        if abs(fc) < epsilon:
            return c

        if f(a) * fc < 0:
            b = c
        else:
            a = c

    return (a + b) / 2
