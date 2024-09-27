""" Api definition
    All validations and mappings should be in the services
"""

from typing import List, Optional

from auth_middleware.functions import require_groups
from auth_middleware.types import User
from fastapi import APIRouter, Body, Depends, Header, Path, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response

from web_api_template.api.v1.addresses.services import ReadService, WriteService
from web_api_template.core.api import ProblemDetail
from web_api_template.core.api.common_query_model import CommonQueryModel
from web_api_template.core.http.validators import (
    ksuid_path_validator,
    ksuid_query_validator,
)
from web_api_template.core.logging import logger
from web_api_template.domain.exceptions import AddressNotFoundException
from web_api_template.domain.value_objects import Address, AddressCreate, AddressFilter

api_router = APIRouter()


@api_router.get(
    "/{person_id}/addresses",
    response_model=List[Address],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ProblemDetail,
        },
    },
    dependencies=[
        Depends(require_groups(["customer"])),
    ],
)
async def get_addresses_by_person(
    request: Request,
    response: Response,
    person_id: str = Path(..., description="The ID of the person"),
) -> List[Address]:
    """Get a list of addresses associated with the person.

    Args:
        request (Request): _description_
        response (Response): _description_
        id (str, optional): _description_. Defaults to Path(..., description="The ID of the person").

    Returns:
        List[Address]: _description_
    """

    # TODO: Filter addresses by status

    logger.debug("Person id: {}", person_id)

    # TODO: generalize filter
    # Check if person exists
    # TODO: create an "exists" method on service

    result: List[Address] = await ReadService().get_list_by_person_id(
        person_id=person_id
    )
    return result


@api_router.post(
    "/{person_id}/addresses",
    response_model=Address,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "model": ProblemDetail,
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ProblemDetail,
        },
        status.HTTP_409_CONFLICT: {
            "model": ProblemDetail,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ProblemDetail,
        },
    },
    dependencies=[
        Depends(require_groups(["customer"])),
    ],
)
async def add_address(
    request: Request,
    response: Response,
    address: AddressCreate,
    person_id: str = Path(..., description="The ID of the person"),
) -> Address:
    """Add a new address to the person.
    - TODO: Check for the existence of the address associated to the person.

    Args:
        request (Request): _description_
        response (Response): _description_
        person (PersonCreate): _description_

    Returns:
        Person: _description_
    """

    # Check if person exists
    # TODO: create an "exists" method on service
    # entity_person: Person = await PersonReadService().get_by_id(id=id)

    # TODO: it is better to have an explicit method for creating a policy with a person id + policy data
    entity: Address = await WriteService().create_for_person(
        # current_user=current_user,
        person_id=person_id,
        request=address,
    )

    return entity
