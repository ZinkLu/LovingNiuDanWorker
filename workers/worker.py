from scripts.printer import print_pipline
from scripts.render import render_docx
from utils.logger import logger

from . import BaseWorker
from .providers.redis_provider import RedisProvider


class Worker(BaseWorker):

    def __init__(self, provider: RedisProvider) -> None:
        self.provider = provider

    def start(self, channel):
        logger.info("worker started!")
        for message_data in self.provider.consume(channel):
            print(message_data)
            out_put = render_docx(message_data)
            print_pipline(out_put.as_posix())

    def stop(self):
        logger.info("worker stopped")
        self.provider.stop()

    @classmethod
    def from_config(cls, worker_cls, *args, **kwargs):
        return cls(worker_cls(*args, **kwargs))
