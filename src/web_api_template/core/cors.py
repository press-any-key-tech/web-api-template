from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .logging import logger
from .settings import settings


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
