import asyncio

import pytest


@pytest.mark.asyncio
async def test_single_subscriber(multisubscriber_queue, event_loop):

    async def producer():
        await asyncio.sleep(.25)
        await multisubscriber_queue.put('test1')
        await multisubscriber_queue.put('test2')
        await multisubscriber_queue.put('test3')
        await multisubscriber_queue.put('test4')
        await multisubscriber_queue.close()

    event_loop.create_task(producer())

    subscriber = multisubscriber_queue.subscribe()
    assert await subscriber.__anext__() == 'test1'
    assert await subscriber.__anext__() == 'test2'
    assert await subscriber.__anext__() == 'test3'
    assert await subscriber.__anext__() == 'test4'
    with pytest.raises(StopAsyncIteration):
        await subscriber.__anext__()

    assert len(multisubscriber_queue) == 0


@pytest.mark.asyncio
async def test_multiple_subscribers(multisubscriber_queue, event_loop):

    async def create_consumer():
        subscriber = multisubscriber_queue.subscribe()
        print(await subscriber.__anext__())
        print(await subscriber.__anext__())

    tasks = list()
    tasks.append(event_loop.create_task(create_consumer()))
    tasks.append(event_loop.create_task(create_consumer()))
    tasks.append(event_loop.create_task(create_consumer()))
    tasks.append(event_loop.create_task(create_consumer()))
    await asyncio.sleep(.25)

    await multisubscriber_queue.put('test')
    assert len(multisubscriber_queue) == 4

    await multisubscriber_queue.close()
    await asyncio.wait(tasks)
    assert len(multisubscriber_queue) == 0
