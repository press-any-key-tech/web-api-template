""" Api definition
    All validations and mappings should be in the services
"""

from fastapi import APIRouter, Depends, HTTPException, status
from starlette.requests import Request

from web_api_template.core.api import ApiMessage
from web_api_template.core.settings import settings

from .response import HealthCheckResponse
from .services import HealthcheckService

api_router = APIRouter()


@api_router.get(
    "/healthcheck",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheckResponse,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ApiMessage,
        },
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": ApiMessage,
        },
    },
)
async def get(
    request: Request,
) -> HealthCheckResponse:
    """
    Healthcheck endpoint for orchestrators
    Do not check database or external services as it could overload the servers

    Returns:
        HealthCheckResponse: health information
    """

    if await HealthcheckService().verify():
        return HealthCheckResponse(status="Healthy", version=settings.PROJECT_VERSION)
    else:
        raise HTTPException(status_code=503, detail="Unhealthy")
