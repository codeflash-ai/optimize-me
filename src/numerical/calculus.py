from typing import List, Tuple, Callable


def numerical_integration_rectangle(
    f: Callable[[float], float], a: float, b: float, n: int
) -> float:
    if a > b:
        a, b = b, a
    h = (b - a) / n
    result = 0.0
    for i in range(n):
        x = a + i * h
        result += f(x)
    return result * h


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
