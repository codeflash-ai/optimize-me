import time
import asyncio


async def retry_with_backoff(func, max_retries=3):
    if max_retries < 1:
        raise ValueError("max_retries must be at least 1")
    last_exception = None
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            last_exception = e
            if attempt < max_retries - 1:
                time.sleep(0.0001 * attempt)
    raise last_exception


async def fetch_user(user_id: int) -> dict:
    """Simulates fetching a user from a database"""
    await asyncio.sleep(0.0001)
    return {"id": user_id, "name": f"User{user_id}"}


async def fetch_all_users(user_ids: list[int]) -> list[dict]:
    return await asyncio.gather(*(fetch_user(user_id) for user_id in user_ids))
