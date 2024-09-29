from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from web_api_template.core.api import ProblemDetail, ValidationErrorDetail
from web_api_template.core.logging import logger


async def http_exception_handler(request: Request, exc: HTTPException):
    """HttpException handler

    Args:
        request (Request): _description_
        exc (HTTPException): _description_

    Returns:
        _type_: _description_
    """

    logger.error(
        f"HTTPException: {exc.status_code} - {exc.detail} - {exc.headers} - {
            exc.detail}"
    )

    problem_detail = ProblemDetail(
        title="An error occurred",
        status=exc.status_code,
        detail=exc.detail,
        instance=str(request.url),
    )
    return JSONResponse(
        status_code=exc.status_code, content=problem_detail.model_dump()
    )


async def general_exception_handler(request: Request, exc: Exception):
    """General exception handler

    Args:
        request (Request): _description_
        exc (Exception): _description_

    Returns:
        _type_: _description_
    """

    logger.exception(f"Exception: {exc}")

    problem_detail = ProblemDetail(
        title="Internal Server Error",
        status=500,
        detail="An unexpected error occurred.",
        instance=str(request.url),
    )
    return JSONResponse(status_code=500, content=problem_detail.model_dump())



async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Validation exception handler

    Args:
        request (Request): _description_
        exc (Exception): _description_

    Returns:
        _type_: _description_
    """

    logger.exception(f"Exception: {exc}")

    errors = [
        ValidationErrorDetail(
            type=error["type"],
            loc=error["loc"],
            msg=error["msg"],
            input=error["input"],
            ctx={k: str(v) for k, v in error.get("ctx", {}).items()} if error.get("ctx") else None,
            url=error.get("url")
        )
        for error in exc.errors()
    ]

    problem_detail = ProblemDetail(
        title="Validation error",
        status=422,
        detail="One or more validation errors occurred.",
        instance=str(request.url),
        errors=errors,
    )

    return JSONResponse(status_code=422, content=problem_detail.model_dump())



