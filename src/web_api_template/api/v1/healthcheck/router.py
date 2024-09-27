""" Api Routes
"""

from fastapi import APIRouter

from . import api

ROUTE_PREFIX: str = "/hc"

api_router = APIRouter()
api_router.include_router(api.api_router, prefix=ROUTE_PREFIX, tags=["HealthCheck"])
