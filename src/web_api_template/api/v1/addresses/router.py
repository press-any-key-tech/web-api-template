""" Api Routes
"""

from fastapi import APIRouter

from . import api_addresses

ROUTE_PREFIX: str = "/api/v1/addresses"

api_router = APIRouter()
api_router.include_router(api_addresses.api_router, prefix=ROUTE_PREFIX, tags=["Addresses"])
