import logging
from utils import config as c 

import logging
import logging.config

logging.config.dictConfig(c.logging)

# create logger
logger = logging.getLogger('simpleExample')

# 'application' code
for i in xrange(100):
    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')