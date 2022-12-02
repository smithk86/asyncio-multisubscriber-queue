from asyncio import Queue
from contextlib import contextmanager
from typing import Any, AsyncGenerator, Generator, Generic, TypeVar, cast

T = TypeVar("T")


class MultisubscriberQueue(Generic[T]):
    """Allow a single producer to provide the same payload to multiple consumers simultaneously.

    An `asyncio.Queue` can be obtained directly by calling MultisubscriberQueue.queue() or
    `MultisubscriberQueue.subscribe()` can be used to yield data as it is available.
    """

    subscribers: set[Queue[T]]
    _close_sentinel: T = cast(T, object())

    __slots__ = ("subscribers",)

    def __init__(self) -> None:
        """The constructor for MultisubscriberQueue class."""
        self.subscribers = {*()}

    def __len__(self) -> int:
        return len(self.subscribers)

    def __contains__(self, q: Queue[T]) -> bool:
        return q in self.subscribers

    async def subscribe(self) -> AsyncGenerator[T, None]:
        """Subscribe to `MultisubscriberQueue` using an async generator.

        Instead of working with the Queue directly, the client can
        subscribe to data and have it yielded as it is available.

        Example:
        ```
        from asyncio_multisubscriber_queue import MultisubscriberQueue

        # create a MultisubscriberQueue for distributing str instances
        mqueue: MultisubscriberQueue[str] = MultisubscriberQueue()
        async with mqueue.subscribe() as data:
                first_item: str = await q.get()
        ```

        Returns:
            AsyncGenerator containing subscriber data.
        """
        with self.queue() as q:
            while True:
                _data: Any = await q.get()
                if _data is self._close_sentinel:
                    break
                yield _data

    def add(self) -> Queue[T]:
        """Get a new Queue which is part of the subscriber set.

        Returns:
            A subscriber Queue.
        """
        queue: Queue[T] = Queue()
        self.subscribers.add(queue)
        return queue

    def remove(self, queue: Queue[T]) -> None:
        """Remove given queue from the subscriber set.

        Args:
            queue: Queue object to be removed from the subscriber set.
        """
        if queue in self.subscribers:
            self.subscribers.remove(queue)

    @contextmanager
    def queue(self) -> Generator[Queue[T], None, None]:
        """Context helper which manages the lifecycle of the subscriber Queue.

        Example:
        ```
        from asyncio import Queue
        from asyncio_multisubscriber_queue import MultisubscriberQueue

        # create a MultisubscriberQueue for distributing int instances
        mqueue: MultisubscriberQueue[int] = MultisubscriberQueue()
        with mqueue.queue() as q:
            first_item: int = await q.get()
        ```

        Returns:
            Generator containing a subscriber Queue.
        """
        _queue = self.add()
        try:
            yield _queue
        finally:
            self.remove(_queue)

    async def put(self, data: T) -> None:
        """Put data on all the Queues in the subscriber set.

        Args:
            data: Data for the Queues.
        """
        for _queue in self.subscribers:
            await _queue.put(data)

    async def close(self) -> None:
        """Put the close sentinel on the Queues.

        This is used to signal the end of the MultisubscriberQueue session.
        """
        await self.put(self._close_sentinel)
