""" Api Routes
"""

from fastapi import APIRouter
from . import api_policies


ROUTE_PREFIX: str = "/api/v1/policies"

api_router = APIRouter()
api_router.include_router(
    api_policies.api_router, prefix=ROUTE_PREFIX, tags=["Policies"]
)
