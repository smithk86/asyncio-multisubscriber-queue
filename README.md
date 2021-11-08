#  asyncio-multisubscriber-queue

MultisubscriberQueue allows a single producer to provide the same payload to multiple consumers simultaniously. An asyncio.Queue is created for each consumer and each call to MultisubscriberQueue.put() iterates over each asyncio.Queue and puts the payload on each queue.

Please see [example.py](https://github.com/smithk86/asyncio-multisubscriber-queue/blob/master/example.py) for a simple example.

## Change Log

### [0.3.0] - 2021-11-08

- Add type hints and type validation with mypy
- Replace _QueueContext object with @contextmanager on MultisubscriberQueue.queue()
