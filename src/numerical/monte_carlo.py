import random


def monte_carlo_pi(num_samples: int) -> float:
    """Estimate π using Monte Carlo method."""
    inside_circle = 0

    for _ in range(num_samples):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)

        if x**2 + y**2 <= 1:
            inside_circle += 1

    return 4 * inside_circle / num_samples
