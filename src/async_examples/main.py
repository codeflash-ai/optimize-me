from asyncio import get_running_loop, sleep


async def hello_world():
    print("Hello")
    await sleep(0)
    return "World"
