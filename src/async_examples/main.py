from asyncio import sleep

async def hello_world():
    print("Hello")
    await sleep(0.002)
    return "World"