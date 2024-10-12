""" Api definition
    All validations and mappings should be in the services
"""

from fastapi import APIRouter, HTTPException, status
from opentelemetry import trace
from starlette.requests import Request

from web_api_template.core.api import ProblemDetail
from web_api_template.core.settings import settings

from .response import HealthCheckResponse
from .services import HealthcheckService

api_router = APIRouter()

# Get tracer
tracer = trace.get_tracer(__name__)


@api_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheckResponse,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ProblemDetail,
        },
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": ProblemDetail,
        },
    },
)
async def get(
    request: Request,
) -> HealthCheckResponse:
    """
    Healthcheck endpoint for orchestrators
    Recommendation: Do not check database or external services as it could overload the servers

    Returns:
        HealthCheckResponse: health information
    """

    with tracer.start_as_current_span("healthcheck-span") as span:
        span.set_attribute("endpoint", "healthcheck")
        span.add_event("Healthcheck started")

        if await HealthcheckService().verify():
            span.add_event("Healthcheck successful")
            return HealthCheckResponse(
                status="Healthy", version=settings.PROJECT_VERSION
            )
        else:
            span.add_event("Healthcheck failed")
            raise HTTPException(status_code=503, detail="Unhealthy")
