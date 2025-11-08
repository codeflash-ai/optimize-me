import asyncio


async def retry_with_backoff(func, max_retries=3):
    if max_retries < 1:
        raise ValueError("max_retries must be at least 1")
    last_exception = None
    # Precompute backoff values outside the loop for faster lookups
    backoffs = [0.0001 * attempt for attempt in range(max_retries)]
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            last_exception = e
            if attempt < max_retries - 1:
                # Use asyncio.sleep instead of time.sleep for non-blocking behavior in async context
                # This avoids blocking the event loop, allowing concurrency and better performance
                await asyncio.sleep(backoffs[attempt])
    raise last_exception
