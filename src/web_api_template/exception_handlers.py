from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from web_api_template.core.api import ProblemDetail


async def http_exception_handler(request: Request, exc: HTTPException):
    """HttpException handler

    Args:
        request (Request): _description_
        exc (HTTPException): _description_

    Returns:
        _type_: _description_
    """
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
    problem_detail = ProblemDetail(
        title="Internal Server Error",
        status=500,
        detail="An unexpected error occurred.",
        instance=str(request.url),
    )
    return JSONResponse(status_code=500, content=problem_detail.model_dump())
