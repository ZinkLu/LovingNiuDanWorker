from abc import abstractmethod
import re
from typing import NoReturn

from win32con import SB_BOTH

from typing import Iterator


class BaseProvider:
    @abstractmethod
    def start_listen(self) -> Iterator[dict]:
        while True:
            yield None
