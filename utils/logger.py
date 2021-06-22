import os
from logging import getLogger, FileHandler, Formatter

logger = getLogger("printer")

h = FileHandler(os.path.join('logs', 'log.log'))
f = Formatter('%(process)d %(filename)s %(levelname)s %(asctime)s %(funcName)s %(message)s')
h.setFormatter(f)
logger.addHandler(h)
