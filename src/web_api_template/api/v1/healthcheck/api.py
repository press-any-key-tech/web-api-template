""" Api definition
    All validations and mappings should be in the services
"""

from auth_middleware.functions import require_groups, require_user
from fastapi import APIRouter, Depends, HTTPException, status
from starlette.requests import Request
from starlette.responses import Response

from web_api_template.api.v1.persons.services import ReadService, WriteService
from web_api_template.core.api import ProblemDetail
from web_api_template.core.api.pagination_query_model import PaginationQueryModel
from web_api_template.core.auth.functions import require_permissions
from web_api_template.core.http.validators import ksuid_path_validator
from web_api_template.core.logging import logger
from web_api_template.core.repository.manager.sqlalchemy.page import Page
from web_api_template.core.settings import settings
from web_api_template.domain.entities.person import Person
from web_api_template.domain.entities.person_create import PersonCreate
from web_api_template.domain.entities.person_filter import PersonFilter

from .response import HealthCheckResponse
from .services import HealthcheckService

api_router = APIRouter()


@api_router.get("/hw")
async def read_main():
    return {"msg": "Hello World"}


@api_router.get(
    "/hc",
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

    return HealthCheckResponse(status="Healthy", version=settings.PROJECT_VERSION)

    # if await HealthcheckService().verify():
    #     logger.debug("Healthcheck successful")
    #     return HealthCheckResponse(status="Healthy", version=settings.PROJECT_VERSION)
    # else:
    #     logger.debug("Healthcheck failed")
    #     raise HTTPException(status_code=503, detail="Unhealthy")


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
