"""
Inefficient async concurrency patterns.
These examples show common anti-patterns that prevent proper concurrent execution.
"""

import asyncio
import time
import random
from concurrent.futures import ThreadPoolExecutor


async def fake_api_call(delay, data):
    """Simulates an API call with network delay"""
    await asyncio.sleep(delay)
    return f"Processed: {data}"


async def cpu_bound_task(n):
    """Simulates CPU-intensive work"""
    result = 0
    for i in range(n):
        result += i ** 2
    return result


async def sequential_api_calls(urls):
    """
    Makes API calls one by one instead of concurrently.
    Should use asyncio.gather() or asyncio.as_completed().
    """
    results = []
    for i, url in enumerate(urls):
        # Sequential execution defeats async purpose
        result = await fake_api_call(random.uniform(0.5, 2.0), url)
        results.append(result)
    return results


async def inefficient_task_creation():
    """
    Creates tasks inefficiently by awaiting each one immediately.
    Should create all tasks first, then await them concurrently.
    """
    results = []
    
    # Anti-pattern: creating and immediately awaiting tasks
    for i in range(10):
        task = asyncio.create_task(fake_api_call(0.5, f"data_{i}"))
        result = await task  # Waits for each task individually
        results.append(result)
    
    return results


async def mixed_blocking_and_async():
    """
    Mixes blocking operations with async, destroying concurrency benefits.
    Should separate blocking operations or use thread pools.
    """
    results = []
    
    for i in range(5):
        # Async operation
        async_result = await fake_api_call(0.3, f"async_{i}")
        results.append(async_result)
        
        # Blocking operation that blocks the entire event loop
        time.sleep(0.5)  # Should use asyncio.sleep() or run in thread
        
        # CPU-bound task that blocks event loop
        cpu_result = sum(range(100000))  # Should use asyncio.to_thread()
        results.append(f"CPU result: {cpu_result}")
    
    return results


async def inefficient_semaphore_usage():
    """
    Uses semaphore inefficiently, limiting concurrency unnecessarily.
    Also has poor error handling that can leak semaphore permits.
    """
    # Semaphore too restrictive - limits to 1 concurrent operation
    semaphore = asyncio.Semaphore(1)
    
    async def limited_task(data):
        await semaphore.acquire()
        try:
            result = await fake_api_call(0.5, data)
            # Potential issue: if this raises, semaphore never released
            if random.random() < 0.1:
                raise Exception("Random failure")
            return result
        finally:
            # Should use 'async with semaphore:' instead
            semaphore.release()
    
    tasks = []
    for i in range(10):
        task = asyncio.create_task(limited_task(f"data_{i}"))
        tasks.append(task)
    
    # Sequential gathering instead of handling exceptions properly
    results = []
    for task in tasks:
        try:
            result = await task
            results.append(result)
        except Exception as e:
            results.append(f"Error: {e}")
    
    return results


async def busy_waiting_pattern():
    """
    Uses busy waiting instead of proper async coordination.
    Should use asyncio.Event, asyncio.Queue, or similar primitives.
    """
    shared_data = {"status": "pending", "result": None}
    
    async def producer():
        # Simulate work
        await asyncio.sleep(2.0)
        shared_data["result"] = "Important data"
        shared_data["status"] = "ready"
    
    async def consumer():
        # Busy waiting - wastes CPU cycles
        while shared_data["status"] != "ready":
            await asyncio.sleep(0.01)  # Polling every 10ms
        
        return shared_data["result"]
    
    # Start producer and consumer
    producer_task = asyncio.create_task(producer())
    result = await consumer()
    await producer_task
    
    return result


async def inefficient_queue_processing():
    """
    Processes queue items sequentially instead of with worker pools.
    Should use multiple workers for concurrent processing.
    """
    queue = asyncio.Queue()
    
    # Fill queue with work items
    for i in range(20):
        await queue.put(f"work_item_{i}")
    
    results = []
    
    # Single worker processing sequentially
    while not queue.empty():
        item = await queue.get()
        # Each item takes time to process
        result = await fake_api_call(0.3, item)
        results.append(result)
        queue.task_done()
    
    return results


async def thread_pool_misuse():
    """
    Misuses thread pools by creating new pools repeatedly.
    Should reuse thread pool and use proper async integration.
    """
    results = []
    
    for i in range(10):
        # Creates new thread pool for each task - inefficient
        with ThreadPoolExecutor(max_workers=1) as executor:
            # Runs simple async-friendly task in thread unnecessarily
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                executor, 
                lambda: time.sleep(0.1) or f"thread_result_{i}"
            )
            results.append(result)
    
    return results


async def race_condition_example():
    """
    Demonstrates race conditions due to improper async coordination.
    Should use locks or other synchronization primitives.
    """
    counter = {"value": 0}
    
    async def increment_counter():
        for _ in range(1000):
            # Race condition: read-modify-write without synchronization
            current = counter["value"]
            await asyncio.sleep(0.001)  # Simulate some async work
            counter["value"] = current + 1
    
    # Run multiple incrementers concurrently
    tasks = [increment_counter() for _ in range(5)]
    await asyncio.gather(*tasks)
    
    # Result will be unpredictable due to race condition
    return counter["value"]  # Should be 5000 but will be less


if __name__ == "__main__":
    async def main():
        print("Running inefficient concurrency examples...")
        
        # Example 1: Sequential API calls
        urls = [f"https://api.example.com/data/{i}" for i in range(5)]
        start_time = time.time()
        results = await sequential_api_calls(urls)
        print(f"Sequential calls took: {time.time() - start_time:.2f}s")
        
        # Example 2: Inefficient task creation
        start_time = time.time()
        results = await inefficient_task_creation()
        print(f"Inefficient tasks took: {time.time() - start_time:.2f}s")
        
        # Example 3: Race condition
        final_count = await race_condition_example()
        print(f"Race condition result: {final_count} (should be 5000)")
    
    asyncio.run(main())