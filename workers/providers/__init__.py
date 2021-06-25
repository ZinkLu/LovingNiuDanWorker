from abc import abstractmethod
from typing import Iterator


class BaseProvider:

    @abstractmethod
    def consume(self, *args) -> Iterator[dict]:
        while True:
            yield None

    @abstractmethod
    def stop(self):
        return
