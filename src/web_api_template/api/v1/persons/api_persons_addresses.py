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

from web_api_template.api.v1.addresses.services import (
    WriteService as AddressWriteService,
)
from web_api_template.api.v1.persons.services import ReadService as PersonReadService
from web_api_template.api.v1.policies.services import ReadService as PolicyReadService
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
from web_api_template.domain.exceptions import PersonNotFoundException
from web_api_template.domain.value_objects import Address, AddressCreate

api_router = APIRouter()


# @api_router.get(
#     "/{id}/policies",
#     response_model=List[Policy],
#     status_code=status.HTTP_200_OK,
#     responses={
#         status.HTTP_500_INTERNAL_SERVER_ERROR: {
#             "model": ProblemDetail,
#         },
#     },
#     dependencies=[
#         Depends(require_groups(["customer"])),
#     ],
# )
# async def get_policies_by_person(
#     request: Request,
#     response: Response,
#     id: str = Path(..., description="The ID of the person"),
# ) -> List[Policy]:
#     """Get a list of policies associated with the person.

#     Args:
#         request (Request): _description_
#         response (Response): _description_
#         id (str, optional): _description_. Defaults to Path(..., description="The ID of the person").

#     Returns:
#         List[Policy]: _description_
#     """

#     # TODO: Filter policies by status

#     status_code: int
#     error_message: dict

#     logger.debug("Person id: {}", id)

#     try:
#         # TODO: generalize filter
#         # Check if person exists
#         # TODO: create an "exists" method on service
#         entity: Person = await ReadService().get_by_id(id=id)

#         result: List[Policy] = await PolicyReadService().get_list_by_person_id(id=id)
#         return result

#     except PersonNotFoundException as e:
#         logger.exception("Person with id {} not found", id)
#         status_code = status.HTTP_404_NOT_FOUND
#         error_message = {"message": str(e)}
#     except Exception as e:
#         logger.exception("Not controlled exception")
#         status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
#         error_message = {"message": f"Something went wrong: {str(e)}"}

#     return JSONResponse(
#         status_code=status_code,
#         content=error_message,
#     )


@api_router.post(
    "/{id}/addresses",
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
    id: str = Path(..., description="The ID of the person"),
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
    entity: Address = await AddressWriteService().create_for_person(
        # current_user=current_user,
        person_id=id,
        request=address,
    )

    return entity


@api_router.delete(
    "/{person_id}/addresses/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "model": ProblemDetail,
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ProblemDetail,
            "description": "Person or address not found",
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
async def delete_address_by_id(
    request: Request,
    response: Response,
    person_id: str,
    id: str,
):
    """Deletes a and address with the specific id.
    - Person should not have any active policies associated with it.

    Args:
        request (Request): _description_
        response (Response): _description_
        person_id (str): _description_
        id (str): _description_

    Returns:
        _type_: _description_
    """

    await AddressWriteService().delete_by_person_and_id(person_id=person_id, id=id)
    return
