import sys
from typing import Tuple


__VERSION__: str = '0.3.0'
__DATE__: str = '2021-11-08'
__MIN_PYTHON__: Tuple[int, int] = (3, 7)


if sys.version_info < __MIN_PYTHON__:
    sys.exit('python {}.{} or later is required'.format(*__MIN_PYTHON__))


from .queue import MultisubscriberQueue
