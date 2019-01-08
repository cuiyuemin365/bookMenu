# -*- coding: utf-8 -*
import sys
from myredis.myredis import *
from log.log import logger
from time import sleep

reload(sys)
sys.setdefaultencoding('utf-8')
if __name__ == '__main__':
    while True:
        print QUEUE_DOUBAN_TAG + ':' + str(MyRedis.get_con().llen(QUEUE_DOUBAN_TAG))
        print QUEUE_DOUBAN_TAG_EXCEPTION + ':' + str(MyRedis.get_con().llen(QUEUE_DOUBAN_TAG_EXCEPTION))
        print QUEUE_DOUBAN_ID + ':' + str(MyRedis.get_con().llen(QUEUE_DOUBAN_ID))
        print QUEUE_DOUBAN_ID_EXCEPTION + ':' + str(MyRedis.get_con().llen(QUEUE_DOUBAN_ID_EXCEPTION))
        print '=============================================================='
        sleep(5)
    # logger.info(MyRedis.get_con().lpop(QUEUE_DOUBAN_ID_EXCEPTION))
    # logger.info(MyRedis.get_con().delete(QUEUE_DOUBAN_TAG_EXCEPTION))
    # logger.info(MyRedis.get_con().delete(QUEUE_DOUBAN_ID_EXCEPTION))
