from time import sleep
from asyncio import sleep as async_sleep, sleep
import asyncio


async def tasked():
    await asyncio.sleep(0.002)
    return "Tasked"
