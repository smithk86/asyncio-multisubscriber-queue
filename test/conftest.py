import pytest

from asyncio_multisubscriber_queue import MultisubscriberQueue


@pytest.fixture
async def multisubscriber_queue(event_loop):
    return MultisubscriberQueue(loop=event_loop)
