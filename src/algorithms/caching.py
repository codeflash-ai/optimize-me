from typing import Callable, Any
import time


def time_based_cache(expiry_seconds: int) -> Callable:
    """Manual implementation of a time-based cache decorator."""

    def decorator(func: Callable) -> Callable:
        cache: dict[tuple, tuple[Any, float]] = {}

        def make_key(args, kwargs) -> tuple:
            if kwargs:
                items = tuple(sorted(kwargs.items()))
                return (args, items)
            return (args, None)

        def wrapper(*args, **kwargs) -> Any:
            key = make_key(args, kwargs)

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
