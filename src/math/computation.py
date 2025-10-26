def gcd_recursive(a: int, b: int) -> int:
    """Calculate greatest common divisor using Euclidean algorithm with recursion."""
    # Tail recursion can be replaced with a loop for better performance.
    while b != 0:
        a, b = b, a % b
    return a
