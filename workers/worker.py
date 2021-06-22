from .providers.redis_provider import RedisProvider
from scripts.printer import print_pipline
from scripts.render import render_docx
from utils.logger import logger


class RedisWorker:
    def __init__(self, redis_provider: RedisProvider) -> None:
        self.redis_provider = redis_provider

    def start(self):
        logger.info("worker started!")
        while message_data := self.redis_provider.start_listen():
            out_put = render_docx(message_data)
            print_pipline(out_put.as_posix())

    def stop(self):
        logger.info("worker stopped")
        self.redis_provider.redis.close()

