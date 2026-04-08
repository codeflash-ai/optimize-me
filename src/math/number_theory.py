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

    is_prime = bytearray(b"\x01") * (n + 1)
    is_prime[0] = is_prime[1] = 0

    if n >= 4:
        is_prime[4 : n + 1 : 2] = b"\x00" * (((n - 4) // 2) + 1)

    for i in range(3, math.isqrt(n) + 1, 2):
        if is_prime[i]:
            start = i * i
            step = i * 2
            is_prime[start : n + 1 : step] = b"\x00" * ((n - start) // step + 1)

    primes = [2] if n >= 2 else []
    primes.extend(i for i in range(3, n + 1, 2) if is_prime[i])
    return primes
