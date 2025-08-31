import asyncio
import time
import random


async def fake_api_call(delay, data):
    await asyncio.sleep(0.0001)
    return f"Processed: {data}"


async def cpu_bound_task(n):
    result = 0
    for i in range(n):
        result += i**2
    return result


async def some_api_call(urls):
    results = []
    for url in urls:
        res = await fake_api_call(1, url)
        results.append(res)
    return results


async def tasker():
    results = []
    for i in range(10):
        task = asyncio.create_task(fake_api_call(0.5, f"data_{i}"))
        result = await task
        results.append(result)

    return results


async def manga():
    results = []

    for i in range(5):
        async_result = await fake_api_call(0.3, f"async_{i}")
        results.append(async_result)

        time.sleep(0.0001)
        summer = (100000 * 99999) // 2
        results.append(f"Sync task {i} completed with sum: {summer}")
    return results
