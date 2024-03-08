import re

from fastapi import HTTPException, Path, Query, status

from web_api_template.core.domain.validators import ksuid_validator


def ksuid_query_validator(
    id: str = Query(..., description="A valid ksuid query parameter")
) -> str:
    return http_ksuid_validator(id)


def ksuid_path_validator(
    id: str = Path(..., description="A valid ksuid path parameter")
) -> str:
    return http_ksuid_validator(id)


def http_ksuid_validator(ksuid: str) -> str:
    """Validates both query and path parameters for a valid KSUID format."""

    try:
        return ksuid_validator(ksuid)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid KSUID format"
        )
