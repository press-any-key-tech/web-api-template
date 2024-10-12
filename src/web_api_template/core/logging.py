import logging
import sys

from loguru import logger
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import SpanKind
from opentelemetry.trace.status import Status, StatusCode

from .settings import settings


# Crear un handler personalizado para OpenTelemetry
class OpenTelemetryHandler(logging.Handler):
    def emit(self, record):
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span(
            "loguru-span", kind=SpanKind.INTERNAL
        ) as span:
            span.set_attribute("loguru.message", record.getMessage())
            span.set_status(Status(StatusCode.OK))
            if record.exc_info:
                span.record_exception(record.exc_info[1])


# Configurar el logger
logger.remove()
logger.add(
    sink=sys.stderr,
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT,
    colorize=True,
)

logger.add(OpenTelemetryHandler(), level=settings.LOG_LEVEL)


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
