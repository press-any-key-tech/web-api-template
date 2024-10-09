""" Api definition
    All validations and mappings should be in the services
"""

from typing import List

from auth_middleware.functions import require_groups
from fastapi import APIRouter, Depends, Path, status
from starlette.requests import Request
from starlette.responses import Response

from web_api_template.api.v1.policies.services import ReadService as PolicyReadService
from web_api_template.api.v1.policies.services import WriteService as PolicyWriteService
from web_api_template.core.api import ProblemDetail
from web_api_template.core.logging import logger
from web_api_template.domain.aggregates import Policy, PolicyCreate

api_router = APIRouter()


@api_router.get(
    "/{person_id}/policies",
    response_model=List[Policy],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ProblemDetail,
        },
    },
    dependencies=[
        Depends(require_groups(["administrator"])),
    ],
)
async def get_policies_by_person(
    request: Request,
    response: Response,
    person_id: str = Path(..., description="The ID of the person"),
) -> List[Policy]:
    """Get a list of policies associated with the person.

    Args:
        request (Request): _description_
        response (Response): _description_
        id (str, optional): _description_. Defaults to Path(..., description="The ID of the person").

    Returns:
        List[Policy]: _description_
    """

    # TODO: Filter policies by status

    logger.debug("Person id: {}", person_id)

    result: List[Policy] = await PolicyReadService().get_list_by_person_id(
        person_id=person_id
    )
    return result


@api_router.post(
    "/{person_id}/policies",
    response_model=Policy,
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
async def create_policy(
    request: Request,
    response: Response,
    policy: PolicyCreate,
    person_id: str = Path(..., description="The ID of the person"),
) -> Policy:
    """Create a new policy for the given person.
    - Check for existence of addresses and policies.

    Args:
        request (Request): _description_
        response (Response): _description_
        person (PersonCreate): _description_

    Returns:
        Person: _description_
    """

    # Check if person exists
    # TODO: create an "exists" method on service

    # TODO: it is better to have an explicit method for creating a policy with a person id + policy data
    entity: Policy = await PolicyWriteService().create_for_person(
        # current_user=current_user,
        person_id=person_id,
        request=policy,
    )

    return entity
