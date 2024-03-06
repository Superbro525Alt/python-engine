import logging
import time

level = logging.DEBUG

logger = logging.getLogger(__name__)
logger.setLevel(level)

ch = logging.StreamHandler()
ch.setLevel(level)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)

logger.addHandler(ch)

fh = logging.FileHandler(f"logs/{time.time()}.log")
fh.setLevel(level)
fh.setFormatter(formatter)

logger.addHandler(fh)

def debug(msg: str):
    logger.debug(msg)

def info(msg: str):
    logger.info(msg)

def warning(msg: str):
    logger.warning(msg)

def error(msg: str):
    logger.error(msg)

def critical(msg: str):
    logger.critical(msg)
    exit()
