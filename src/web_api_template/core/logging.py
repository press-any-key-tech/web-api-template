import sys

from loguru import logger

from .settings import settings

# Configurar el logger
logger.remove()
logger.add(
    sink=sys.stderr,
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT,
    colorize=True,
)
