""" Api definition
    All validations and mappings should be in the services
"""


from auth_middleware.functions import require_groups
from fastapi import APIRouter, Depends, status
from starlette.requests import Request
from starlette.responses import Response

from web_api_template.api.v1.addresses.services import ReadService, WriteService
from web_api_template.core.api import ProblemDetail
from web_api_template.core.http.validators import (
    ksuid_path_validator,
)
from web_api_template.domain.value_objects import Address, AddressCreate

api_router = APIRouter()


@api_router.get(
    "/{id}",
    response_model=Address,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ProblemDetail,
            "description": "Address not found",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ProblemDetail,
            "description": "Internal server error",
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
) -> Address:
    """Get a address by id

    Args:
        request (Request): _description_
        response (Response): _description_
        id (str): _description_

    Returns:
        Address: _description_
    """

    entity: Address = await ReadService().get_by_id(id=id)
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
    """Deletes a address with the specific id.
    - Address should not have any active policies associated with it.

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
    response_model=Address,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_409_CONFLICT: {
            "model": ProblemDetail,
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ProblemDetail,
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
        Depends(require_groups(["customer"])),
        Depends(ksuid_path_validator),
    ],
)
async def update(
    request: Request,
    response: Response,
    id: str,
    address: AddressCreate,
) -> Address:
    """Update the address with the given information.
    - Do not allow to dissasociate any active polcies from the address.

    Args:
        request (Request): _description_
        response (Response): _description_
        id (str): _description_
        pot_request (AddressCreate): _description_

    Returns:
        Address: _description_
    """

    entity: Address = await WriteService().update(
        id=id,
        # current_user=current_user,
        request=address,
    )

    return entity
