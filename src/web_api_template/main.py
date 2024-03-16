from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pythondi import Provider, configure

from web_api_template.core.auth.auth_middleware import AuthMiddleware
from web_api_template.core.logging import logger
from web_api_template.core.repository.manager.sqlalchemy.database import Database
from web_api_template.core.repository.model.sqlalchemy import metadata
from web_api_template.core.settings import settings
from web_api_template.di import include_di
from web_api_template.routes import include_routers


def include_cors(app: FastAPI):
    """
    Include CORS configuration
    """

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=settings.CORS_ALLOWED_METHODS,
        allow_headers=settings.CORS_ALLOWED_HEADERS,
    )

    logger.debug("CORS initialized")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Asynchronous initilizations on startup/shutdown
    Substitute old app.on_event("startup")
    """

    # Initialize SQLALCHEMY database
    await Database.initialize()

    # # TODO: send database initialization to a module
    # if settings.INITIALIZE_DATABASE:

    #     from web_api_template.core.repository.model.dynamodb.settings import (
    #         settings as dynamodb_settings,
    #     )

    #     if dynamodb_settings.DYNAMODB_REPOSITORY:
    #         logger.debug("Initializing DYNAMODB database ...")
    #         raise NotImplementedError("DynamoDB initialization not implemented yet")

    logger.info("Async initializations completed ...")

    yield


def start_application(app: FastAPI):
    """
    Start the application launching all required modules
    """

    # Dependency injection (general)
    provider: Provider = Provider()
    include_di(provider=provider)
    configure(provider=provider)

    include_cors(app)
    include_routers(app)

    # TODO: Add middleware
    app.add_middleware(AuthMiddleware)

    app.router.lifespan_context = lifespan

    return app


# Initialize application
app: FastAPI = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
start_application(app)
