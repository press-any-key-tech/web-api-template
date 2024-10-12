from auth_middleware.jwt_auth_middleware import JwtAuthMiddleware
from auth_middleware.providers.cognito.cognito_provider import CognitoProvider
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from pydilite import Provider, configure
from transaction_middleware import TransactionMiddleware

from web_api_template.core.logging import logger
from web_api_template.core.settings import settings
from web_api_template.di import include_di
from web_api_template.exception_handlers import (
    general_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from web_api_template.lifespan import lifespan
from web_api_template.routes import include_routers


def start_application(app: FastAPI):
    """
    Start the application launching all required modules
    """

    # ----------------------------------------
    # OpenTelemetry instrumentation
    # ----------------------------------------

    logger.debug("Initializing OpenTelemetry")
    resource = Resource.create(attributes={"service.name": settings.OTEL_SERVICE_NAME})
    trace_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(trace_provider)

    otlp_exporter = OTLPSpanExporter(
        endpoint=settings.OTEL_EXPORTER_OTLP_ENDPOINT, insecure=True
    )
    span_processor = BatchSpanProcessor(otlp_exporter)
    trace_provider.add_span_processor(span_processor)

    # FastAPI instrumentation
    FastAPIInstrumentor.instrument_app(app)
    logger.debug("OpenTelemetry initialized")

    # ----------------------------------------
    # Dependency injection
    # ----------------------------------------
    provider: Provider = Provider()
    include_di(provider=provider)
    configure(provider=provider)

    # ----------------------------------------
    # Exception handling
    # ----------------------------------------
    app.add_exception_handler(Exception, general_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)

    # ----------------------------------------
    # Middlewares
    # ----------------------------------------

    # Add middlewares (in order of desired execution)

    # CORS should be the first middleware (if needed)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=settings.CORS_ALLOWED_METHODS,
        allow_headers=settings.CORS_ALLOWED_HEADERS,
    )
    logger.debug("CORS initialized")

    # AuthMiddleware (creates current_user). Requires auth provider
    app.add_middleware(JwtAuthMiddleware, auth_provider=CognitoProvider())
    logger.debug("Auth middleware initialized")

    # TransactionMiddleware (creates transaction_id)
    app.add_middleware(TransactionMiddleware)
    logger.debug("Transaction middleware initialized")

    # ----------------------------------------
    # Lifespan (startup/shutdown async actions)
    # ----------------------------------------
    app.router.lifespan_context = lifespan

    # ----------------------------------------
    # Application routers
    # ----------------------------------------

    include_routers(app)

    return app
