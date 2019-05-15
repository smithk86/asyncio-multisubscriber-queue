import asyncio
from asyncio import Queue, wait_for


class MultisubscriberQueue(object):

    def __init__(self, loop=None):
        self.loop = loop if loop else asyncio.get_running_loop()
        self.subscribers = list()

    def __len__(self):
        return len(self.subscribers)

    def __contains__(self, q):
        return q in self.subscribers

    async def subscribe(self):
        with _QueueContext(self) as q:
            while True:
                val = await q.get()
                if val is StopAsyncIteration:
                    break
                else:
                    yield val

    def queue(self):
        q = Queue(loop=self.loop)
        self.subscribers.append(q)
        return q

    def remove(self, q):
        if q in self.subscribers:
            self.subscribers.remove(q)
        else:
            raise KeyError('subscriber queue does not exist')

    async def put(self, val):
        for q in self.subscribers:
            await q.put(val)

    async def close(self):
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
