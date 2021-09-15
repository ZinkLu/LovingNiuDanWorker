import os
from logging import FileHandler, Formatter, getLogger

logger = getLogger("printer")
logger.setLevel("INFO")

if not os.path.exists("logs"):
    os.mkdir("logs")

h = FileHandler(os.path.join('logs', 'log.log'))
f = Formatter('%(asctime)s - %(levelname)s - %(message)s')
h.setFormatter(f)
logger.addHandler(h)

if __name__ == '__main__':
    logger.info("test")
