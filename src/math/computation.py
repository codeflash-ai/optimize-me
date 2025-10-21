def gcd_recursive(a: int, b: int) -> int:
    """Calculate greatest common divisor using Euclidean algorithm with recursion."""
    # Use an iterative approach to eliminate recursive call overhead
    while b:
        a, b = b, a % b
    return a
