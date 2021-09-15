import json

from redis import StrictRedis
from utils.logger import logger
from workers.providers import BaseProvider


class RedisProvider(BaseProvider):

    def __init__(self, host, port, password, db, **kwargs):
        logger.info("start to establish to redis {host} {port} {password} {db}".format(host=host,
                                                                                       port=port,
                                                                                       password=password,
                                                                                       db=db))
        redis = StrictRedis(
            host=host,
            port=port,
            db=db,
            password=password,
            socket_keepalive=True,
        )
        self.redis = redis

    def consume(self, channel) -> dict:
        self.pubsub = self.redis.pubsub()
        logger.info('start to listen to channel {}'.format(channel))
        self.pubsub.subscribe(channel)
        for message in self.pubsub.listen():
            if message['data'] == 1:
                continue
            yield json.loads(message['data'])

    def stop(self):
        print("closing redis provider...")
        self.pubsub.close()
        self.redis.close()
        print("redis provider closed!")
