from typing import Callable, Any
import time


def time_based_cache(expiry_seconds: int) -> Callable:
    """Manual implementation of a time-based cache decorator."""

    def decorator(func: Callable) -> Callable:
        cache: dict[str, tuple[Any, float]] = {}

        def wrapper(*args, **kwargs) -> Any:
            # Optimize key construction by using tuple for args and a tuple of sorted items for kwargs
            # This avoids unnecessary repr() string conversions and string joins
            if kwargs:
                key = (args, tuple(sorted(kwargs.items())))
            else:
                key = (args, None)

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
