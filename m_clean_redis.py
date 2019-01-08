# -*- coding: utf-8 -*
import sys
from myredis.myredis import *
from log.log import logger
from time import sleep

reload(sys)
sys.setdefaultencoding('utf-8')
if __name__ == '__main__':
    logger.info(MyRedis.get_con().delete(QUEUE_DOUBAN_TAG))
    logger.info(MyRedis.get_con().delete(QUEUE_DOUBAN_TAG_EXCEPTION))
    logger.info(MyRedis.get_con().delete(QUEUE_DOUBAN_ID))
    logger.info(MyRedis.get_con().delete(QUEUE_DOUBAN_ID_EXCEPTION))
    print '=============================finished================================='
