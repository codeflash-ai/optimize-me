import aiohttp
import time
import asyncio


async def get_endpoint(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url) as response:
        return await response.text()


async def some_api_call(urls):
    async with aiohttp.ClientSession() as session:
        results = []
        for url in urls:
            result = await get_endpoint(session, url)
            results.append(result)
        return results
    return None


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
                time.sleep(0.00001 * attempt)
    raise last_exception


async def sorter(arr):
    print("codeflash stdout: Sorting list")
    await asyncio.sleep(0.00001)
    # Use Python's built-in Timsort for maximal performance and memory efficiency
    arr.sort()
    print(f"result: {arr}")
    return arr


async def task():
    return "done"
