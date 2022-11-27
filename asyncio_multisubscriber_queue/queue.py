from asyncio import Queue
from contextlib import contextmanager
from typing import Any, AsyncGenerator, Generator, Generic, TypeVar, cast


T = TypeVar("T")


class MultisubscriberQueue(Generic[T]):
    subscribers: list[Queue[T]]

    __slots__ = ("subscribers",)

    def __init__(self) -> None:
        """
        The constructor for MultisubscriberQueue class

        """
        self.subscribers = list()

    def __len__(self) -> int:
        return len(self.subscribers)

    def __contains__(self, q: Queue[T]) -> bool:
        return q in self.subscribers

    async def subscribe(self) -> AsyncGenerator[T, None]:
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
    def queue(self) -> Generator[Queue[T], None, None]:
        """
        Get a new async Queue which is tracked and garbage collected
        when the context is concluded

        """
        _queue: Queue[T] = Queue()
        try:
            self.subscribers.append(_queue)
            yield _queue
        finally:
            self.subscribers.remove(_queue)

    def remove(self, queue: Queue[T]) -> None:
        """
        Remove queue from the pool of subscribers

        """
        if queue in self.subscribers:
            self.subscribers.remove(queue)

    async def put(self, data: T) -> None:
        """
        Put new data on all subscriber queues

        """
        for _queue in self.subscribers:
            await _queue.put(data)

    async def close(self) -> None:
        """
        Force clients using MultisubscriberQueue.subscribe() to end iteration

        """
        await self.put(cast(T, StopAsyncIteration))
