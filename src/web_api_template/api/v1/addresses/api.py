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


# @api_router.get(
#     "/",
#     response_model=List[Address],
#     status_code=status.HTTP_200_OK,
#     responses={
#         status.HTTP_500_INTERNAL_SERVER_ERROR: {
#             "model": ProblemDetail,
#             "description": "Internal Server Error",
#         },
#     },
#     dependencies=[
#         Depends(require_groups(["customer"])),
#     ],
# )
# async def get_list(
#     request: Request,
#     response: Response,
#     list_filter: AddressFilter = Depends(),
#     query: CommonQueryModel = Depends(),
# ) -> List[Address] | JSONResponse:
#     """Get a list of policies

#     Args:
#         request (Request): _description_
#         response (Response): _description_

#     Returns:
#         List[Address] | JSONResponse: _description_
#     """

#     status_code: int
#     error_message: dict

#     try:
#         result: List[Address] = await ReadService().get_list(filter=list_filter)
#         return result

#     except Exception as e:
#         logger.exception("Not controlled exception")
#         status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
#         error_message = {"message": f"Something went wrong: {str(e)}"}

#     return JSONResponse(
#         status_code=status_code,
#         content=error_message,
#     )


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
) -> Address | JSONResponse:
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
) -> Address | JSONResponse:
    """Update the address with the given information.
    - Do not allow to dissasociate any active polcies from the address.

    Args:
        request (Request): _description_
        response (Response): _description_
        id (str): _description_
        pot_request (AddressCreate): _description_

    Returns:
        Address | JSONResponse: _description_
    """

    entity: Address = await WriteService().update(
        id=id,
        # current_user=current_user,
        request=address,
    )

    return entity


# @api_router.post(
#     "/",
#     response_model=Address,
#     status_code=status.HTTP_201_CREATED,
#     responses={
#         status.HTTP_403_FORBIDDEN: {
#             "model": ProblemDetail,
#         },
#         status.HTTP_400_BAD_REQUEST: {
#             "model": ProblemDetail,
#         },
#         status.HTTP_409_CONFLICT: {
#             "model": ProblemDetail,
#         },
#         status.HTTP_500_INTERNAL_SERVER_ERROR: {
#             "model": ProblemDetail,
#             "description": "Internal Server Error",
#         },
#     },
#     dependencies=[
#         Depends(require_groups(["customer"])),
#     ],
# )
# async def create(
#     request: Request,
#     response: Response,
#     address: AddressCreate,
# ) -> Address | JSONResponse:
#     """Create a new address with the given information.
#     - Check for existence of addresses and policies.

#     Args:
#         request (Request): _description_
#         response (Response): _description_
#         address (AddressCreate): _description_

#     Returns:
#         Address | JSONResponse: _description_
#     """

#     status_code: int
#     error_message: dict

#     try:

#         entity: Address = await WriteService().create(
#             # current_user=current_user,
#             request=address,
#         )

#         return entity

#     # except NotAllowedCreationException as e:
#     #     logger.exception("You are not allowed to create this item")
#     #     status_code = status.HTTP_403_FORBIDDEN
#     #     error_message = {"message": str(e)}

#     # except (
#     #     ItemNotFoundException,
#     # ) as e:
#     #     logger.exception("Controlled exception")
#     #     status_code = status.HTTP_400_BAD_REQUEST
#     #     error_message = {"message": str(e)}

#     except AddressNotFoundException as e:
#         logger.exception("Address with id {} not found", id)
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
