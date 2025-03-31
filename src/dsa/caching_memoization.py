from typing import Callable, Any
import time


def time_based_cache(expiry_seconds: int) -> Callable:
    """Manual implementation of a time-based cache decorator."""

    def decorator(func: Callable) -> Callable:
        cache: dict[str, tuple[Any, float]] = {}

        def wrapper(*args, **kwargs) -> Any:
            key_parts = [repr(arg) for arg in args]
            key_parts.extend(f"{k}:{repr(v)}" for k, v in sorted(kwargs.items()))
            key = ":".join(key_parts)

            current_time = time.time()

            if key in cache:
                result, timestamp = cache[key]
                if current_time - timestamp < expiry_seconds:
                    return result

            result = func(*args, **kwargs)

            cache[key] = (result, current_time)

            return result

        return wrapper

    return decorator


def matrix_chain_order(matrices: list[tuple[int, int]]) -> int:
    """
    Find the minimum number of operations needed to multiply a chain of matrices.

    Args:
        matrices: A list of matrix dimensions as tuples (rows, cols)

    Returns:
        Minimum number of operations
    """
    n = len(matrices)

    def dp(i: int, j: int) -> int:
        if i == j:
            return 0

        min_ops = float("inf")

        for k in range(i, j):
            cost = (
                dp(i, k)
                + dp(k + 1, j)
                + matrices[i][0] * matrices[k][1] * matrices[j][1]
            )
            min_ops = min(min_ops, cost)

        return min_ops

    return dp(0, n - 1)


def binomial_coefficient(n: int, k: int) -> int:
    if k == 0 or k == n:
        return 1
    return binomial_coefficient(n - 1, k - 1) + binomial_coefficient(n - 1, k)


def coin_change(coins: list[int], amount: int, index: int) -> int:
    if amount == 0:
        return 1
    if amount < 0 or index >= len(coins):
        return 0

    return coin_change(coins, amount - coins[index], index) + coin_change(
        coins, amount, index + 1
    )


def knapsack(weights: list[int], values: list[int], capacity: int, n: int) -> int:
    if n == 0 or capacity == 0:
        return 0

    if weights[n - 1] > capacity:
        return knapsack(weights, values, capacity, n - 1)

    return max(
        values[n - 1] + knapsack(weights, values, capacity - weights[n - 1], n - 1),
        knapsack(weights, values, capacity, n - 1),
    )