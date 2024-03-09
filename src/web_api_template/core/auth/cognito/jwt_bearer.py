from typing import Optional

from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN

from .cognito_client import CognitoClient
from .jw_types import JWTAuthorizationCredentials
from .settings import settings


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[JWTAuthorizationCredentials]:
        if settings.AUTH_DISABLED:
            return None

        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if credentials:
            # TODO: use a constant for the string "Bearer"
            if credentials.scheme != "Bearer":
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Wrong authentication method"
                )

            jwt_token = credentials.credentials

            message, signature = jwt_token.rsplit(".", 1)

            try:
                jwt_credentials = JWTAuthorizationCredentials(
                    jwt_token=jwt_token,
                    header=jwt.get_unverified_header(jwt_token),
                    claims=jwt.get_unverified_claims(jwt_token),
                    signature=signature,
                    message=message,
                )
            except JWTError:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="JWK-invalid"
                )

            # TODO: perhaps this checks are a bit too excessive...
            if "token_use" not in jwt_credentials.claims:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="JWK invalid"
                )

            if not CognitoClient().verify_token(jwt_credentials):
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="JWK_invalid"
                )

            return jwt_credentials
