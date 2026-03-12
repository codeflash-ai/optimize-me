import random


def monte_carlo_pi(num_samples: int) -> float:
    """Estimate π using Monte Carlo method."""
    inside_circle = 0

    # Handle edge cases: negative or zero num_samples
    if num_samples <= 0:
        return 4 * inside_circle / num_samples

    # Process pairs of samples per loop iteration to reduce loop overhead.
    limit = num_samples - (num_samples & 1)  # largest even <= num_samples
    for _ in range(0, limit, 2):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x * x + y * y <= 1:
            inside_circle += 1

        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x * x + y * y <= 1:
            inside_circle += 1

    # Handle the remaining sample when num_samples is odd.
    if num_samples & 1:
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x * x + y * y <= 1:
            inside_circle += 1

    return 4 * inside_circle / num_samples
