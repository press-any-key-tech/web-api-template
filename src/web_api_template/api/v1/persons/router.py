""" Api Routes
"""

from fastapi import APIRouter

from . import api_persons, api_persons_addresses

ROUTE_PREFIX: str = "/api/v1/persons"

api_router = APIRouter()
api_router.include_router(api_persons.api_router, prefix=ROUTE_PREFIX, tags=["Persons"])
api_router.include_router(
    api_persons_addresses.api_router, prefix=ROUTE_PREFIX, tags=["PersonsAddresses"]
)
