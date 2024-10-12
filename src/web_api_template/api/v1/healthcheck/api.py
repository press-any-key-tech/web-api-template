""" Api definition
    All validations and mappings should be in the services
"""

from fastapi import APIRouter, HTTPException, status
from starlette.requests import Request

from web_api_template.core.api import ProblemDetail
from web_api_template.core.logging import logger
from web_api_template.core.settings import settings

from .response import HealthCheckResponse
from .services import HealthcheckService

api_router = APIRouter()


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

    logger.debug("Healthcheck started")

    if await HealthcheckService().verify():
        logger.debug("Healthcheck successful")
        return HealthCheckResponse(status="Healthy", version=settings.PROJECT_VERSION)
    else:
        logger.debug("Healthcheck failed")
        raise HTTPException(status_code=503, detail="Unhealthy")
