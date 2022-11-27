#!/usr/bin/env python

import asyncio

from asyncio_multisubscriber_queue import MultisubscriberQueue


async def main() -> None:
    """An example showing the MultisubscriberQueue in action."""

    async def consumer(name: str) -> None:
        async for data in mqueue.subscribe():
            print(f"{name}: {data}")

    mqueue: MultisubscriberQueue[str] = MultisubscriberQueue()

    # setup consumer tasks
    tasks = []
    for i in range(5):
        tasks.append(asyncio.create_task(consumer(f"consumer {i}")))
    await asyncio.sleep(0.5)  # wait half a second for consumers to be ready

    # produce messages to the multisubscriber queue
    await mqueue.put("first message")
    await asyncio.sleep(0.5)
    await mqueue.put("second message")
    await asyncio.sleep(0.5)
    await mqueue.put("third message")
    await asyncio.sleep(0.5)

    # for subscribers to disconnect
    await mqueue.close()

    # wait for the tasks to end
    await asyncio.wait(tasks)

    # subscriber count is zero
    assert len(mqueue) == 0


if __name__ == "__main__":
    asyncio.run(main())
