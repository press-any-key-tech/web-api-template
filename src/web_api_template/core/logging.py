import contextvars
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

# Create a context variable to store the trace_id
trace_id_context = contextvars.ContextVar("trace_id", default=None)


def add_trace_id(record) -> bool:
    """Add the trace_id to the log record

    Args:
        record (_type_): _description_
    """
    trace_id = trace_id_context.get()
    record["extra"]["trace_id"] = trace_id if trace_id else "N/A"
    return True  # Return True to indicate the filter passed


# Create a handler to send the logs to OpenTelemetry
class OpenTelemetryHandler(logging.Handler):
    def emit(self, record) -> None:
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span(
            "loguru-span", kind=SpanKind.INTERNAL
        ) as span:
            span.set_attribute("loguru.message", record.getMessage())
            span.set_status(Status(StatusCode.OK))
            if record.exc_info:
                span.record_exception(record.exc_info[1])


# Configure the logger
logger.remove()

# stderr Logger
logger.add(
    sink=sys.stderr,
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT,
    filter=add_trace_id,
    colorize=True,
    serialize=False,
    backtrace=True,
    diagnose=True,
    enqueue=True,
)

# OpenTelemetry Logger
logger.add(
    OpenTelemetryHandler(),
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT,
    filter=add_trace_id,
)


__all__ = [
    "logger",
    "trace_id_context",
]  # Add logger and trace_id_context to __all__ to be able to import them from the package


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
