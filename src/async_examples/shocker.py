from time import sleep
from asyncio import sleep


async def tasked():
    return "Tasked"


def tasked_2():
    sleep(0.00002)
    return "Tasked"
