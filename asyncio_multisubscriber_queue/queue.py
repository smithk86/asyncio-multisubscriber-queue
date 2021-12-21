from __future__ import annotations

import asyncio
from asyncio import Queue, wait_for
from contextlib import contextmanager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, AsyncGenerator, Generator, List


class MultisubscriberQueue:
    def __init__(self):
        """
        The constructor for MultisubscriberQueue class

        """
        self.subscribers: List[Queue] = list()

    def __len__(self) -> int:
        return len(self.subscribers)

    def __contains__(self, q: Queue) -> bool:
        return q in self.subscribers

    async def subscribe(self) -> AsyncGenerator:
        """
        Subscribe to data using an async generator

        Instead of working with the Queue directly, the client can
        subscribe to data and have it yielded directly.

        Example:
            with MultisubscriberQueue.subscribe() as data:
                print(data)

        """
        with self.queue() as q:
            while True:
                _data: Any = await q.get()
                if _data is StopAsyncIteration:
                    break
                else:
                    yield _data

    @contextmanager
    def queue(self) -> Generator:
        """
        Get a new async Queue which is tracked and garbage collected
        when the context is concluded

        """
        _queue: Queue = Queue()
        try:
            self.subscribers.append(_queue)
            yield _queue
        finally:
            self.subscribers.remove(_queue)

    def remove(self, queue: Queue) -> None:
        """
        Remove queue from the pool of subscribers

        """
        if queue in self.subscribers:
            self.subscribers.remove(queue)

    async def put(self, data: Any) -> None:
        """
        Put new data on all subscriber queues

        """
        for _queue in self.subscribers:
            await _queue.put(data)

    async def close(self) -> None:
        """
        Force clients using MultisubscriberQueue.subscribe() to end iteration

        """
        await self.put(StopAsyncIteration)
