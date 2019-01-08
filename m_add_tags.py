# -*- coding: utf-8 -*
import sys
from myredis.myredis import *

reload(sys)
sys.setdefaultencoding('utf-8')
if __name__ == '__main__':
    tags = [u'科普', u'互联网', u'编程', u'操作系统',
            u'交互设计', u'用户体验', u'算法', u'科技',
            'web', 'UE', u'通信', 'java', u'设计模式', u'数据库', u'python', u'程序']
    MyRedis.get_con().lpush(QUEUE_DOUBAN_TAG, *tags)
    print '=============================finished================================='
