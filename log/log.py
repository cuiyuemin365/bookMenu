import logging
import logging.config
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
# sys.path.append('..')

CONF_LOG = "logging.conf"
logging.config.fileConfig(CONF_LOG)
logger = logging.getLogger()

if __name__ == '__main__':
    e = Exception("asdc")
    logger.info('adsca%s', e)
