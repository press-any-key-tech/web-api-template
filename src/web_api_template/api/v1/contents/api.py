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

from web_api_template.api.v1.contents.services import ReadService, WriteService
from web_api_template.core.api import ApiMessage
from web_api_template.core.api.common_query_model import CommonQueryModel
from web_api_template.core.api.utils import get_content_type
from web_api_template.core.http.validators import (
    ksuid_path_validator,
    ksuid_query_validator,
)
from web_api_template.core.logging import logger
from web_api_template.domain.entities import Content, ContentCreate, ContentFilter
from web_api_template.domain.exceptions import ContentNotFoundException

api_router = APIRouter()


@api_router.get(
    "/",
    response_model=List[Content],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ApiMessage,
        },
    },
    dependencies=[
        Depends(require_groups(["customer"])),
    ],
)
async def get_list(
    request: Request,
    response: Response,
    list_filter: ContentFilter = Depends(),
    query: CommonQueryModel = Depends(),
) -> List[Content] | JSONResponse:
    """Get a list of policies

    Args:
        request (Request): _description_
        response (Response): _description_

    Returns:
        List[Content] | JSONResponse: _description_
    """

    status_code: int
    error_message: dict

    try:
        result: List[Content] = await ReadService().get_list(filter=list_filter)
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
    response_model=Content,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ApiMessage,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ApiMessage,
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
) -> Content | JSONResponse:
    """Get a content by id

    Args:
        request (Request): _description_
        response (Response): _description_
        id (str): _description_

    Returns:
        Content: _description_
    """

    status_code: int
    error_message: dict

    try:
        entity: Content = await ReadService().get_by_id(id=id)
        return entity
    except ContentNotFoundException as e:
        logger.exception("Content with id {} not found", id)
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
    """Deletes a content with the specific id.
    - Content should not have any active policies associated with it.

    Args:
        request (Request): _description_
        response (Response): _description_
        id (str): _description_

    Returns:
        _type_: _description_
    """

    error_message: dict

    try:
        await WriteService().delete_by_id(id=id)
        return
    except ContentNotFoundException as e:
        logger.exception("Content with id {} not found", id)
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
    dependencies=[
        Depends(require_groups(["customer"])),
        Depends(ksuid_path_validator),
    ],
)
async def update(
    request: Request,
    response: Response,
    id: str,
    content: ContentCreate,
) -> Content | JSONResponse:
    """Update the content with the given information.
    - Do not allow to dissasociate any active polcies from the content.

    Args:
        request (Request): _description_
        response (Response): _description_
        id (str): _description_
        pot_request (ContentCreate): _description_

    Returns:
        Content | JSONResponse: _description_
    """

    status_code: int
    error_message: dict

    logger.debug("update request: {}", content)

    try:
        entity: Content = await WriteService().update(
            id=id,
            # current_user=current_user,
            request=content,
        )

        return entity

    except ContentNotFoundException as e:
        logger.exception("Content with id {} not found", id)
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
    response_model=Content,
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
    dependencies=[
        Depends(require_groups(["customer"])),
    ],
)
async def create(
    request: Request,
    response: Response,
    content: ContentCreate,
) -> Content | JSONResponse:
    """Create a new content with the given information.
    - Check for existence of addresses and policies.

    Args:
        request (Request): _description_
        response (Response): _description_
        content (ContentCreate): _description_

    Returns:
        Content | JSONResponse: _description_
    """

    status_code: int
    error_message: dict

    try:

        entity: Content = await WriteService().create(
            # current_user=current_user,
            request=content,
        )

        return entity

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

    except ContentNotFoundException as e:
        logger.exception("Content with id {} not found", id)
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
