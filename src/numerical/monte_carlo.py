import random


def monte_carlo_pi(num_samples: int) -> float:
    """Estimate π using Monte Carlo method."""
    inside_circle = 0

    # Process two samples per loop iteration to reduce loop overhead.
    for i in range(0, num_samples, 2):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x * x + y * y <= 1:
            inside_circle += 1

        if i + 1 < num_samples:
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)
            if x * x + y * y <= 1:
                inside_circle += 1

    return 4 * inside_circle / num_samples
