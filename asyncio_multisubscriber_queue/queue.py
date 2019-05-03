import asyncio
from asyncio import Queue, wait_for
from uuid import uuid4


class MultisubscriberQueue(object):

    def __init__(self, maxsize=0, loop=None):
        self.maxsize = maxsize
        self.loop = loop
        self.subscribers = dict()

    def __len__(self):
        return len(self.subscribers)

    def __contains__(self, _id):
        return _id in self.subscribers

    def __getitem__(self, _id):
        return self.subscribers[_id]

    async def subscribe(self, timeout=0, timeout_value=None):
        _id, q = self.new()
        try:
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
        finally:
            self.remove(_id)

    def new(self):
        q = Queue(maxsize=self.maxsize, loop=self.loop)
        _id = str(uuid4())
        self.subscribers[_id] = q
        return (_id, q)

    def remove(self, _id):
        if _id in self.subscribers:
            self.subscribers.pop(_id)
        else:
            raise KeyError(f'subscriber id is invalid: {_id}')

    async def put(self, val):
        for q in self.subscribers.values():
            await q.put(val)

    async def close(self):
        await self.put(StopAsyncIteration)
