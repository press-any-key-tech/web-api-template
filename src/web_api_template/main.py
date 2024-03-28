from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydilite import Provider, configure

from web_api_template.core.auth.jwt_auth_middleware import JwtAuthMiddleware
from web_api_template.core.auth.providers.entraid.jwt_bearer_manager import (
    JWTBearerManager,
)
from web_api_template.core.cors import include_cors
from web_api_template.core.logging import logger
from web_api_template.core.repository.manager.sqlalchemy.database import Database
from web_api_template.core.repository.model.sqlalchemy import metadata
from web_api_template.core.settings import settings
from web_api_template.di import include_di
from web_api_template.lifespan import lifespan
from web_api_template.routes import include_routers


def start_application(app: FastAPI):
    """
    Start the application launching all required modules
    """

    # ----------------------------------------
    # Dependency injection
    # ----------------------------------------
    provider: Provider = Provider()
    include_di(provider=provider)
    configure(provider=provider)

    # ----------------------------------------
    # Middlewares
    # ----------------------------------------

    # Add middlewares (in order of desired execution)

    # CORS should be the first middleware (if needed)
    include_cors(app)

    # AuthMiddleware (creates current_user). Requires auth provider
    app.add_middleware(JwtAuthMiddleware, jwt_bearer_manager=JWTBearerManager())

    # AuditMiddleware (requires current_user)

    # ----------------------------------------
    # Lifespan (startup/shutdown async actions)
    # ----------------------------------------
    app.router.lifespan_context = lifespan

    # ----------------------------------------
    # Application routers
    # ----------------------------------------

    include_routers(app)

    return app


app: FastAPI = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)
start_application(app)
