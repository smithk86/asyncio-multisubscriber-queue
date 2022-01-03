#!/usr/bin/env python

import asyncio

from asyncio_multisubscriber_queue import MultisubscriberQueue


async def main():
    async def consumer(name):
        async for data in mqueue.subscribe():
            print(f"{name}: {data}")

    loop = asyncio.get_running_loop()
    mqueue = MultisubscriberQueue()

    # setup consumer tasks
    tasks = list()
    for i in range(5):
        tasks.append(loop.create_task(consumer(f"consumer {i}")))
    await asyncio.sleep(0.5)  # wait half a second for consumers to be ready

    # produce messages to the multisubscriber queue
    await mqueue.put("first message")
    await asyncio.sleep(0.5)
    await mqueue.put("second message")
    await asyncio.sleep(0.5)
    await mqueue.put("third message")
    await asyncio.sleep(0.5)

    # for subscribers to disconnect
    await mqueue.put(StopAsyncIteration)

    # wait for the tasks to end
    await asyncio.wait(tasks)


if __name__ == "__main__":
    asyncio.run(main())
