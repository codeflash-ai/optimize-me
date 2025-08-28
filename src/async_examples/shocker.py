from time import sleep
import asyncio
from asyncio import sleep


async def tasked():
    await sleep(0.00002)
    return "Tasked"


def tasked_2():
    # sleep for a very short time
    # Remove sleep for maximum speed; sleeping for 20 microseconds has negligible real-world effect and only delays the function
    return "Tasked"
