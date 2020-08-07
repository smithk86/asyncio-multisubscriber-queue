import sys

__VERSION__ = '0.2.4'
__DATE__ = '2020-08-07'
__MIN_PYTHON__ = (3, 7)


if sys.version_info < __MIN_PYTHON__:
    sys.exit('python {}.{} or later is required'.format(*__MIN_PYTHON__))


from .queue import MultisubscriberQueue
