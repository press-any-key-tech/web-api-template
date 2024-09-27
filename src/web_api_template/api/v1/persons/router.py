""" Api Routes
"""

from fastapi import APIRouter

from . import api_addresses, api_persons, api_policies

ROUTE_PREFIX: str = "/api/v1/persons"

api_router = APIRouter()
api_router.include_router(api_persons.api_router, prefix=ROUTE_PREFIX, tags=["Persons"])
api_router.include_router(
    api_addresses.api_router, prefix=ROUTE_PREFIX, tags=["Persons"]
)
api_router.include_router(
    api_policies.api_router, prefix=ROUTE_PREFIX, tags=["Persons"]
)
