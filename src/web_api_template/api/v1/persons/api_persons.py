""" Api definition
    All validations and mappings should be in the services
"""

from typing import List, Optional

from auth_middleware.functions import require_groups, require_user
from auth_middleware.types import User
from fastapi import APIRouter, Body, Depends, Header, Path, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response

from web_api_template.api.v1.persons.services import ReadService, WriteService
from web_api_template.core.api import ProblemDetail
from web_api_template.core.api.common_query_model import CommonQueryModel
from web_api_template.core.api.utils import get_content_type
from web_api_template.core.http.validators import (
    ksuid_path_validator,
    ksuid_query_validator,
)
from web_api_template.core.logging import logger
from web_api_template.domain.entities.person import Person
from web_api_template.domain.entities.person_create import PersonCreate
from web_api_template.domain.entities.person_filter import PersonFilter
from web_api_template.domain.exceptions import (
    PersonHasActivePoliciesException,
    PersonNotFoundException,
)

api_router = APIRouter()


@api_router.get(
    "/",
    response_model=List[Person],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ProblemDetail,
            "description": "Internal Server Error",
        },
    },
    dependencies=[
        # Depends(require_groups(["customer", "administrator"])),
        Depends(require_user()),
    ],
)
async def get_list(
    request: Request,
    response: Response,
    list_filter: PersonFilter = Depends(),
    query: CommonQueryModel = Depends(),
) -> List[Person] | JSONResponse:
    """Get a list of persons

    Args:
        request (Request): _description_
        response (Response): _description_

    Returns:
        List[Person] | JSONResponse: _description_
    """

    result: List[Person] = await ReadService().get_list(filter=list_filter)
    return result


@api_router.get(
    "/{id}",
    response_model=Person,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ProblemDetail,
            "description": "Person not found",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ProblemDetail,
            "description": "Internal Server Error",
        },
    },
    dependencies=[
        Depends(require_groups(["customer"])),
        Depends(ksuid_path_validator),
    ],
)
async def get_by_id(
    request: Request,
    response: Response,
    id: str,
) -> Person | JSONResponse:
    """Get a person by id

    Args:
        request (Request): _description_
        response (Response): _description_
        id (str): _description_

    Returns:
        Person: _description_
    """

    entity: Person = await ReadService().get_by_id(id=id)
    return entity


@api_router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "model": ProblemDetail,
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ProblemDetail,
            "description": "Person not found",
        },
        status.HTTP_409_CONFLICT: {
            "model": ProblemDetail,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ProblemDetail,
            "description": "Internal Server Error",
        },
    },
    dependencies=[
        Depends(require_groups(["customer"])),
        Depends(ksuid_path_validator),
    ],
)
async def delete_by_id(
    request: Request,
    response: Response,
    id: str,
):
    """Deletes a person with the specific id.
    - Person should not have any active policies associated with it.

    Args:
        request (Request): _description_
        response (Response): _description_
        id (str): _description_

    Returns:
        _type_: _description_
    """

    await WriteService().delete_by_id(id=id)
    return


@api_router.put(
    "/{id}",
    response_model=Person,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_409_CONFLICT: {
            "model": ProblemDetail,
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ProblemDetail,
            "description": "Person not found",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ProblemDetail,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ProblemDetail,
            "description": "Internal Server Error",
        },
    },
    dependencies=[
        # Depends(require_groups(["customer"])),
        Depends(require_user()),
        Depends(ksuid_path_validator),
    ],
)
async def update(
    request: Request,
    response: Response,
    id: str,
    person: PersonCreate,
) -> Person | JSONResponse:
    """Update the person with the given information.
    - Do not allow to dissasociate any active polcies from the person.

    Args:
        request (Request): _description_
        response (Response): _description_
        id (str): _description_
        pot_request (PersonCreate): _description_

    Returns:
        Person | JSONResponse: _description_
    """

    logger.debug("update request: {}", person)

    entity: Person = await WriteService().update(
        id=id,
        # current_user=current_user,
        request=person,
    )

    return entity


@api_router.post(
    "/",
    response_model=Person,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ProblemDetail,
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ProblemDetail,
        },
        status.HTTP_409_CONFLICT: {
            "model": ProblemDetail,
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ProblemDetail,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ProblemDetail,
            "description": "Internal Server Error",
        },
    },
    dependencies=[
        Depends(require_groups(["customer"])),
    ],
)
async def create(
    request: Request,
    response: Response,
    person: PersonCreate,
) -> Person | JSONResponse:
    """Create a new person with the given information.
    - Check for existence of addresses and policies.

    Args:
        request (Request): _description_
        response (Response): _description_
        person (PersonCreate): _description_

    Returns:
        Person | JSONResponse: _description_
    """

    entity: Person = await WriteService().create(
        # current_user=current_user,
        request=person,
    )

    return entity
