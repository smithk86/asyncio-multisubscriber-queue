# add the project directory to the pythonpath
import path_patch

import pytest  # type: ignore

from asyncio_multisubscriber_queue import MultisubscriberQueue


@pytest.fixture
async def multisubscriber_queue():
    return MultisubscriberQueue()
