import random


def monte_carlo_pi(num_samples: int) -> float:
    """Estimate π using Monte Carlo method."""
    # Use local variable lookups for functions used in loop (reduces attribute lookup in tight loop)
    uniform = random.uniform

    inside_circle = 0

    # Use local variable for accumulator
    rng = (-1.0, 1.0)
    for _ in range(num_samples):
        x = uniform(*rng)
        y = uniform(*rng)
        if x * x + y * y <= 1.0:
            inside_circle += 1

    return 4 * inside_circle / num_samples
