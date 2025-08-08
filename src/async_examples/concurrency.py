import asyncio
import time
import random


async def fake_api_call(delay, data):
    await asyncio.sleep(delay)
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


async def inefficient_task_creation():
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

        time.sleep(0.5)
        cpu_result = sum(range(100000))
        results.append(f"CPU result: {cpu_result}")

    return results
