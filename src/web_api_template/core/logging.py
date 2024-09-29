import logging
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

__all__ = ["logger"]  # Add logger to __all__ to be able to import it from the package


class InterceptHandler(logging.Handler):
    """Redirect logs from sqlalchemy to loguru

    Args:
        logging (_type_): _description_
    """

    def emit(self, record):
        # Get loguru logger
        loguru_logger = logger.opt(depth=6, exception=record.exc_info)
        # Redirect the logs to loguru
        loguru_logger.log(record.levelname, record.getMessage())


# Configure the logging level for sqlalchemy
logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
