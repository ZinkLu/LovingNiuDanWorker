import os
from logging import FileHandler, Formatter, getLogger

logger = getLogger("printer")
logger.setLevel("INFO")

h = FileHandler(os.path.join('logs', 'log.log'))
f = Formatter(
    '%(process)d %(filename)s %(levelname)s %(asctime)s %(funcName)s %(message)s'
)
h.setFormatter(f)
logger.addHandler(h)

if __name__ == '__main__':
    logger.info("test")
