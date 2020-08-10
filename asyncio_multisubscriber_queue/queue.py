import asyncio
from asyncio import Queue, wait_for
from typing import Any


class MultisubscriberQueue(object):
    def __init__(self, **kwargs):
        """
        The constructor for MultisubscriberQueue class

        """
        super().__init__()
        self.subscribers = list()

    def __len__(self):
        return len(self.subscribers)

    def __contains__(self, q):
        return q in self.subscribers

    async def subscribe(self):
        """
        Subscribe to data using an async generator

        Instead of working with the Queue directly, the client can
        subscribe to data and have it yielded directly.

        Example:
            with MultisubscriberQueue.subscribe() as data:
                print(data)

        """
        with self.queue_context() as q:
            while True:
                val = await q.get()
                if val is StopAsyncIteration:
                    break
                else:
                    yield val

    def queue(self):
        """
        Get a new async Queue

        """
        q = Queue()
        self.subscribers.append(q)
        return q

    def queue_context(self):
        """
        Get a new queue context wrapper

        The queue context wrapper allows the queue to be automatically removed
        from the subscriber pool when the context is exited.

        Example:
            with MultisubscriberQueue.queue_context() as q:
                await q.get()

        """
        return _QueueContext(self)

    def remove(self, q):
        """
        Remove queue from the pool of subscribers

        """
        if q in self.subscribers:
            self.subscribers.remove(q)
        else:
            raise KeyError('subscriber queue does not exist')

    async def put(self, data: Any):
        """
        Put new data on all subscriber queues

        Parameters:
            data: queue data

        """
        for q in self.subscribers:
            await q.put(data)

    async def close(self):
        """
        Force clients using MultisubscriberQueue.subscribe() to end iteration

        """
        await self.put(StopAsyncIteration)


class _QueueContext(object):
    def __init__(self, parent):
        self.parent = parent
        self.queue = None

    def __enter__(self):
        self.queue = self.parent.queue()
        return self.queue

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.parent.remove(self.queue)
