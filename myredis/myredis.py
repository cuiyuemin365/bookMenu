# -*- coding: utf-8 -*
import redis
from config.config import Config

cfg = Config.get_cfg()
redis_host = cfg.get("redis", "host")
redis_port = cfg.get("redis", "port")

QUEUE_DOUBAN_TAG = 'queue_douban_tag'
QUEUE_DOUBAN_ID = 'queue_douban_id'
QUEUE_DOUBAN_TAG_EXCEPTION = 'queue_douban_tag_exception'
QUEUE_DOUBAN_ID_EXCEPTION = 'queue_douban_id_exception'


class MyRedis:
    @staticmethod
    def get_con():
        return redis.Redis(host=redis_host, port=redis_port, db=0)
