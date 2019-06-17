import pytest

from asyncio_multisubscriber_queue import MultisubscriberQueue


@pytest.fixture
async def multisubscriber_queue():
    return MultisubscriberQueue()
