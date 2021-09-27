from pprint import pformat

from configs.config import Config
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
            logger.info("获取新的打印任务！")
            logger.info("打印信息：\n%s", pformat(message_data))
            logger.info("正在渲染模板中.....")
            out_put = render_docx(message_data)
            logger.info("模板渲染完成.....")
            logger.info("正在调用打印服务.....")
            print_pipline(out_put.as_posix(), times=Config.get_config("times"), sleep=Config.get_config('sleep'))
            logger.info("打印完成.....")

    def stop(self):
        logger.info("worker stopped")
        self.provider.stop()

    @classmethod
    def from_config(cls, worker_cls, *args, **kwargs):
        return cls(worker_cls(*args, **kwargs))
