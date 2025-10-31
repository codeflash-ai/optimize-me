from typing import List
import math


def gcd_recursive(a: int, b: int) -> int:
    """Calculate greatest common divisor using Euclidean algorithm with recursion."""
    while b != 0:
        a, b = b, a % b
    return a


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
