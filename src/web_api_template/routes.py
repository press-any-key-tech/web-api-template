"""Module to include the API routers for the application
"""

from fastapi import FastAPI

# Healthcheck (do not touch)
from web_api_template.api.healthcheck.api_healthcheck import (
    api_router as healthcheck_router,
)
from web_api_template.api.v1.persons.router import api_router as persons_v1_router
from web_api_template.api.v1.policies.router import api_router as policies_v1_router
from web_api_template.core.logging import logger


def include_routers(app: FastAPI):
    """Include routers for every application

    Args:
        app (_type_): _description_
    """
    logger.debug("Including routers")

    # Healthcheck route (do not touch)
    app.include_router(healthcheck_router)

    app.include_router(persons_v1_router)
    app.include_router(policies_v1_router)
