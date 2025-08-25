import aiohttp
import time

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
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception:
            if attempt < max_retries - 1:
                time.sleep(0.00001 * attempt)
    raise
