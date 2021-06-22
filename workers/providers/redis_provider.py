import json

from redis import StrictRedis

from . import BaseProvider
from utils.logger import logger


class RedisProvider(BaseProvider):
    def __init__(self, redis: StrictRedis) -> None:
        self.redis = redis
        self.pubsub = redis.pubsub()

    @classmethod
    def make_redis_provider(
        cls,
        host,
        port,
        password,
        db,
        **kwargs,
    ) -> "RedisProvider":
        logger.info(
            "start to establish to redis {host} {port} {password} {db}".format(
                host=host,
                port=port,
                password=password,
                db=db,
            ), )
        return cls(
            StrictRedis(
                host=host,
                port=port,
                db=db,
                password=password,
                **kwargs,
            ))

    def start_listen(self, channel) -> dict:
        logger.info('start to listen to channel {}'.format(channel))
        self.pubsub.subscribe(channel)
        for message in self.pubsub.listen():
            yield json.loads(message)
