import logging, os
from .config import CONFIG

_LEVEL = os.getenv("MEGA_LOG_LEVEL", CONFIG.logging.level)
_FMT = CONFIG.logging.format

logging.basicConfig(level=_LEVEL, format=_FMT)


def get_logger(name: str):
    return logging.getLogger(name)
