import asyncio
from asyncio import Queue, wait_for


class MultisubscriberQueue(object):

    def __init__(self, maxsize=0, loop=None):
        self.maxsize = maxsize
        self.loop = loop if loop else asyncio.get_running_loop()
        self.subscribers = list()

    def __len__(self):
        return len(self.subscribers)

    def __contains__(self, q):
        return q in self.subscribers

    def queue(self):
        return _QueueContext(self)

    async def subscribe(self, timeout=0, timeout_value=None):
        with self.queue() as q:
            while True:
                if timeout > 0:
                    try:
                        val = await wait_for(q.get(), timeout=timeout)
                    except asyncio.TimeoutError:
                        if timeout_value:
                            val = timeout_value
                else:
                    val = await q.get()

                if val is StopAsyncIteration:
                    break
                else:
                    yield val

    def new(self):
        q = Queue(maxsize=self.maxsize, loop=self.loop)
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
        self.queue = self.parent.new()
        return self.queue

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.parent.remove(self.queue)
