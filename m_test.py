# -*- coding: utf-8 -*
import sys
from config.config import Config
from mydb.mydb import DBSession
from myredis.myredis import *
from model.model import *

reload(sys)
sys.setdefaultencoding('utf-8')


# if __name__ == '__main__':
#     cfg = Config.get_cfg()
#     print cfg.get('db','host')


# if __name__ == '__main__':
#     session = DBSession()
#     session.close()


def test001():
    result = BookTag.add_if_absent('asdfva')
    print result


if __name__ == '__main__':
    test001()
