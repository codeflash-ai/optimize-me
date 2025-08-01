from time import sleep


async def hello_world():
    print("Hello")
    sleep(0.001)
    return "World"