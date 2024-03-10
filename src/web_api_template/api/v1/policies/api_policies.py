""" Api definition
    All validations and mappings should be in the services
"""

from typing import List, Optional

from fastapi import APIRouter, Body, Depends, Header, Path, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response

from web_api_template.api.v1.contents.services import ReadService as ContentReadService
from web_api_template.api.v1.policies.services import ReadService, WriteService
from web_api_template.core.api import ApiMessage
from web_api_template.core.api.common_query_model import CommonQueryModel
from web_api_template.core.api.utils import get_content_type
from web_api_template.core.auth.cognito.group_checker import GroupChecker
from web_api_template.core.auth.cognito.user import User
from web_api_template.core.auth.cognito.utils import get_current_active_user
from web_api_template.core.http.validators import (
    ksuid_path_validator,
    ksuid_query_validator,
)
from web_api_template.core.logging import logger
from web_api_template.domain.entities import Policy, PolicyCreate, PolicyFilter
from web_api_template.domain.entities.content import Content
from web_api_template.domain.exceptions import (
    PolicyIsActiveException,
    PolicyNotFoundException,
)

# Permissions
allow_customer_group: GroupChecker = GroupChecker(["customer"])
allow_administrator_group: GroupChecker = GroupChecker(["administrator"])


api_router = APIRouter()


@api_router.get(
    "/",
    response_model=List[Policy],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ApiMessage,
        },
    },
    dependencies=[Depends(allow_customer_group)],
)
async def get_list(
    request: Request,
    response: Response,
    current_user: User = Depends(get_current_active_user),
    list_filter: PolicyFilter = Depends(),
    query: CommonQueryModel = Depends(),
) -> List[Policy] | JSONResponse:
    """Get a list of policies

    Args:
        request (Request): _description_
        response (Response): _description_
        current_user (User, optional): _description_. Defaults to Depends(get_current_active_user).

    Returns:
        List[Policy] | JSONResponse: _description_
    """

    status_code: int
    error_message: dict

    logger.debug("Current user: %s", current_user)

    try:
        result: List[Policy] = await ReadService().get_list(filter=list_filter)
        return result

    except Exception as e:
        logger.exception("Not controlled exception")
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        error_message = {"message": f"Something went wrong: {str(e)}"}

    return JSONResponse(
        status_code=status_code,
        content=error_message,
    )


@api_router.get(
    "/{id}",
    response_model=Policy,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ApiMessage,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ApiMessage,
        },
    },
    dependencies=[Depends(allow_customer_group), Depends(ksuid_path_validator)],
)
async def get_by_id(
    request: Request,
    response: Response,
    id: str,
    current_user: User = Depends(get_current_active_user),
) -> Policy | JSONResponse:
    """Get a policy by id

    Args:
        request (Request): _description_
        response (Response): _description_
        id (str): _description_
        current_user (User, optional): _description_. Defaults to Depends(get_current_active_user).

    Returns:
        Policy: _description_
    """

    status_code: int
    error_message: dict

    logger.debug("Current user: %s", current_user)

    try:
        entity: Policy = await ReadService().get_by_id(id=id)
        return entity
    except PolicyNotFoundException as e:
        logger.exception(f"Policy with id {id} not found")
        status_code = status.HTTP_404_NOT_FOUND
        error_message = {"message": str(e)}
    except Exception as e:
        logger.exception("Not controlled exception")
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        error_message = {"message": f"Something went wrong: {str(e)}"}

    return JSONResponse(
        status_code=status_code,
        content=error_message,
    )


@api_router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "model": ApiMessage,
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ApiMessage,
        },
        status.HTTP_409_CONFLICT: {
            "model": ApiMessage,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ApiMessage,
        },
    },
    dependencies=[Depends(allow_administrator_group), Depends(ksuid_path_validator)],
)
async def delete_by_id(
    request: Request,
    response: Response,
    id: str,
    current_user: User = Depends(get_current_active_user),
):
    """Deletes a policy with the specific id.
    - Policy should not have any active policies associated with it.

    Args:
        request (Request): _description_
        response (Response): _description_
        id (str): _description_
        current_user (User, optional): _description_. Defaults to Depends(get_current_active_user).

    Returns:
        _type_: _description_
    """

    error_message: dict

    logger.debug("Current user: %s", current_user)

    try:
        await WriteService().delete_by_id(id=id)
        return
    except PolicyIsActiveException as e:
        logger.exception(f"Policy with id {id} is active and cannot be deleted")
        status_code = status.HTTP_409_CONFLICT
        error_message = {"message": str(e)}
    except PolicyNotFoundException as e:
        logger.exception(f"Policy with id {id} not found")
        status_code = status.HTTP_404_NOT_FOUND
        error_message = {"message": str(e)}
    except Exception as e:
        logger.exception("Not controlled exception")
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        error_message = {"message": f"Something went wrong: {str(e)}"}

    return JSONResponse(
        status_code=status_code,
        content=error_message,
    )


@api_router.put(
    "/{id}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_409_CONFLICT: {
            "model": ApiMessage,
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ApiMessage,
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ApiMessage,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ApiMessage,
        },
    },
    dependencies=[Depends(allow_administrator_group), Depends(ksuid_path_validator)],
)
async def update(
    request: Request,
    response: Response,
    id: str,
    policy: PolicyCreate,
    # current_user: User = Depends(get_current_active_user),
) -> Policy:
    """Update the policy with the given information.
    - Do not allow to dissasociate any active polcies from the policy.

    Args:
        request (Request): _description_
        response (Response): _description_
        id (str): _description_
        pot_request (PolicyCreate): _description_

    Returns:
        Policy | JSONResponse: _description_
    """

    status_code: int
    error_message: dict

    logger.debug("update request: %s", policy)

    try:
        response: Policy = await WriteService().update(
            id=id,
            # current_user=current_user,
            request=policy,
        )

        return response

    except PolicyNotFoundException as e:
        logger.exception(f"Policy with id {id} not found")
        status_code = status.HTTP_404_NOT_FOUND
        error_message = {"message": str(e)}
    except Exception as e:
        logger.exception("Not controlled exception")
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        error_message = {"message": f"Something went wrong: {str(e)}"}

    return JSONResponse(
        status_code=status_code,
        content=error_message,
    )


@api_router.post(
    "/",
    response_model=Policy,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "model": ApiMessage,
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ApiMessage,
        },
        status.HTTP_409_CONFLICT: {
            "model": ApiMessage,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ApiMessage,
        },
    },
    dependencies=[Depends(allow_administrator_group)],
)
async def create(
    request: Request,
    response: Response,
    policy: PolicyCreate,
    current_user: User = Depends(get_current_active_user),
) -> Policy | JSONResponse:
    """Create a new policy with the given information.
    - Check for existence of addresses and policies.

    Args:
        request (Request): _description_
        response (Response): _description_
        policy (PolicyCreate): _description_
        current_user (User, optional): _description_. Defaults to Depends(get_current_active_user).

    Returns:
        Policy | JSONResponse: _description_
    """

    status_code: int
    error_message: dict

    try:

        response: Policy = await WriteService().create(
            # current_user=current_user,
            request=policy,
        )

        return response

    # except NotAllowedCreationException as e:
    #     logger.exception("You are not allowed to create this item")
    #     status_code = status.HTTP_403_FORBIDDEN
    #     error_message = {"message": str(e)}

    # except (
    #     ItemNotFoundException,
    # ) as e:
    #     logger.exception("Controlled exception")
    #     status_code = status.HTTP_400_BAD_REQUEST
    #     error_message = {"message": str(e)}

    except PolicyNotFoundException as e:
        logger.exception(f"Policy with id {id} not found")
        status_code = status.HTTP_404_NOT_FOUND
        error_message = {"message": str(e)}
    except Exception as e:
        logger.exception("Not controlled exception")
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        error_message = {"message": f"Something went wrong: {str(e)}"}

    return JSONResponse(
        status_code=status_code,
        content=error_message,
    )
