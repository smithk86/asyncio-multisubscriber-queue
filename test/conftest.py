# add the project directory to the pythonpath
import os.path
import sys
from pathlib import Path
dir_ = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(dir_.parent))


import pytest

from asyncio_multisubscriber_queue import MultisubscriberQueue


@pytest.fixture
async def multisubscriber_queue():
    return MultisubscriberQueue()
