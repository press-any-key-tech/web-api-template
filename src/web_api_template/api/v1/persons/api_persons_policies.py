""" Api definition
    All validations and mappings should be in the services
"""

from typing import List, Optional

from fastapi import APIRouter, Body, Depends, Header, Path, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response

from web_api_template.api.v1.persons.services import ReadService, WriteService
from web_api_template.api.v1.policies.services import ReadService as PolicyReadService
from web_api_template.api.v1.policies.services import WriteService as PolicyWriteService
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
from web_api_template.domain.entities import Person, PersonCreate, PersonFilter
from web_api_template.domain.entities.policy import Policy
from web_api_template.domain.entities.policy_create import PolicyCreate
from web_api_template.domain.exceptions import (
    PersonHasActivePoliciesException,
    PersonNotFoundException,
    PolicyNotFoundException,
)

# Permissions
allow_customer_group: GroupChecker = GroupChecker(["customer"])
allow_administrator_group: GroupChecker = GroupChecker(["administrator"])


api_router = APIRouter()


@api_router.get(
    "/{id}/policies",
    response_model=List[Policy],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ApiMessage,
        },
    },
    dependencies=[Depends(allow_customer_group)],
)
async def get_policies_by_person(
    request: Request,
    response: Response,
    current_user: User = Depends(get_current_active_user),
    id: str = Path(..., description="The ID of the person"),
) -> List[Policy] | JSONResponse:
    """Get a list of policies associated with the person.

    Args:
        request (Request): _description_
        response (Response): _description_
        current_user (User, optional): _description_. Defaults to Depends(get_current_active_user).
        id (str, optional): _description_. Defaults to Path(..., description="The ID of the person").

    Returns:
        List[Policy] | JSONResponse: _description_
    """

    # TODO: Filter policies by status

    status_code: int
    error_message: dict

    logger.debug("Current user: %s", current_user)
    logger.debug("Person id: %s", id)

    try:
        # TODO: generalize filter
        # Check if person exists
        # TODO: create an "exists" method on service
        entity: Person = await ReadService().get_by_id(id=id)

        result: List[Policy] = await PolicyReadService().get_list_by_person_id(id=id)
        return result

    except PersonNotFoundException as e:
        logger.exception(f"Person with id {id} not found")
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
    "/{id}/policies",
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
async def create_policy(
    request: Request,
    response: Response,
    policy: PolicyCreate,
    id: str = Path(..., description="The ID of the person"),
    current_user: User = Depends(get_current_active_user),
) -> Policy | JSONResponse:
    """Create a new policy for the given person.
    - Check for existence of addresses and policies.

    Args:
        request (Request): _description_
        response (Response): _description_
        person (PersonCreate): _description_
        current_user (User, optional): _description_. Defaults to Depends(get_current_active_user).

    Returns:
        Person | JSONResponse: _description_
    """

    status_code: int
    error_message: dict

    try:

        # Check if person exists
        # TODO: create an "exists" method on service
        entity: Person = await ReadService().get_by_id(id=id)

        policy.person_id = entity.id

        # TODO: it is better to have an explicit method for creating a policy with a person id + policy data
        response: policy = await PolicyWriteService().create(
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

    except PersonNotFoundException as e:
        logger.exception(f"Person with id {id} not found")
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
