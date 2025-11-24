from typing import Callable, Any
import time


def time_based_cache(expiry_seconds: int) -> Callable:
    """Manual implementation of a time-based cache decorator."""

    def decorator(func: Callable) -> Callable:
        cache: dict[str, tuple[Any, float]] = {}

        def wrapper(*args, **kwargs) -> Any:
            # Use args, and sorted tuple of kwargs items as cache key for fast hashing
            if kwargs:
                key = (args, tuple(sorted(kwargs.items())))
            else:
                key = args

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
