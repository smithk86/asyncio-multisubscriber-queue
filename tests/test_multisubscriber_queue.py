import asyncio
from typing import Any, TypeVar

import pytest

from asyncio_multisubscriber_queue import MultisubscriberQueue


def test_queue() -> None:
    queue: MultisubscriberQueue[Any] = MultisubscriberQueue()
    assert len(queue) == 0
    with queue.queue() as q:
        assert type(q) is asyncio.Queue
        assert len(queue) == 1
    assert len(queue) == 0


@pytest.mark.asyncio
async def test_single_subscriber() -> None:
    queue: MultisubscriberQueue[str] = MultisubscriberQueue()

    async def producer() -> None:
        await asyncio.sleep(0.25)
        await queue.put("test1")
        await queue.put("test2")
        await queue.put("test3")
        await queue.put("test4")
        await queue.close()

    asyncio.create_task(producer())

    subscriber = queue.subscribe()
    assert await anext(subscriber) == "test1"
    assert await anext(subscriber) == "test2"
    assert await anext(subscriber) == "test3"
    assert await anext(subscriber) == "test4"
    with pytest.raises(StopAsyncIteration):
        await anext(subscriber)

    assert len(queue) == 0


@pytest.mark.asyncio
async def test_multiple_subscribers() -> None:
    queue: MultisubscriberQueue[int] = MultisubscriberQueue()

    async def create_consumer() -> None:
        subscriber = queue.subscribe()
        await anext(subscriber)
        await anext(subscriber)

    tasks: set[asyncio.Task[None]] = {*()}
    tasks.add(asyncio.create_task(create_consumer()))
    tasks.add(asyncio.create_task(create_consumer()))
    tasks.add(asyncio.create_task(create_consumer()))
    tasks.add(asyncio.create_task(create_consumer()))
    await asyncio.sleep(0.25)

    await queue.put(1338)
    assert len(queue) == 4

    await queue.close()
    await asyncio.wait(tasks)
    assert len(queue) == 0


@pytest.mark.asyncio
async def test_single_subscriber_superclass() -> None:
    T = TypeVar("T")

    class EnumeratedQueue(asyncio.Queue[T]):
        put_count: int = 0

        async def put(self, item: T) -> None:
            EnumeratedQueue.put_count += 1
            await super().put(item)

    class CustomMultisubscriberQueue(MultisubscriberQueue[T]):
        __queue_class__ = EnumeratedQueue

    queue: CustomMultisubscriberQueue[str] = CustomMultisubscriberQueue()

    async def producer() -> None:
        await asyncio.sleep(0.25)
        await queue.put("test1")
        await queue.put("test2")
        await queue.put("test3")
        await queue.put("test4")
        await queue.close()

    assert EnumeratedQueue.put_count == 0

    asyncio.create_task(producer())

    subscriber = queue.subscribe()
    assert await anext(subscriber) == "test1"
    assert await anext(subscriber) == "test2"
    assert await anext(subscriber) == "test3"
    assert await anext(subscriber) == "test4"
    with pytest.raises(StopAsyncIteration):
        await anext(subscriber)

    assert EnumeratedQueue.put_count == 5
    assert len(queue) == 0
