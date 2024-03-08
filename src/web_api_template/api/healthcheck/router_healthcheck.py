""" Api Routes
"""
from fastapi import APIRouter
from . import api_healthcheck

api_router = APIRouter()
api_router.include_router(api_healthcheck.api_router, tags=["Health Check"])
