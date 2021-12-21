#  asyncio-multisubscriber-queue

[![PyPI version](https://img.shields.io/pypi/v/asyncio-multisubscriber-queue)](https://pypi.org/project/asyncio-multisubscriber-queue/)
[![Python Versions](https://img.shields.io/pypi/pyversions/asyncio-multisubscriber-queue)](https://pypi.org/project/asyncio-multisubscriber-queue/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![](https://github.com/smithk86/asyncio-multisubscriber-queue/workflows/pytest/badge.svg)](https://github.com/smithk86/asyncio-multisubscriber-queue/actions?query=workflow%3Apytest)

## Usage

MultisubscriberQueue allows a single producer to provide the same payload to multiple consumers simultaniously. An asyncio.Queue is created for each consumer and each call to MultisubscriberQueue.put() iterates over each asyncio.Queue and puts the payload on each queue.

Please see [example.py](https://github.com/smithk86/asyncio-multisubscriber-queue/blob/master/example.py) for a simple example.

## Change Log

### [0.3.1] - 2021-12-21

- Change build system from setuptools to poetry

### [0.3.0] - 2021-11-08

- Add type hints and type validation with mypy
- Replace _QueueContext object with @contextmanager on MultisubscriberQueue.queue()
