from typing import List, Optional

from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN

from web_api_template.core.auth.invalid_token_exception import InvalidTokenException
from web_api_template.core.auth.jwt_auth_provider import JWTAuthProvider
from web_api_template.core.logging import logger

from .settings import settings
from .types import JWTAuthorizationCredentials


class JWTBearerManager(HTTPBearer):

    def __init__(
        self,
        auth_provider: JWTAuthProvider,
        auto_error: bool = True,
    ):
        super().__init__(auto_error=auto_error)
        self.auth_provider = auth_provider

    async def get_credentials(
        self, request: Request
    ) -> Optional[JWTAuthorizationCredentials]:
        if settings.AUTH_DISABLED:
            return None

        try:
            credentials: Optional[HTTPAuthorizationCredentials] = (
                await super().__call__(request)
            )
        except HTTPException as e:
            logger.error("Error in JWTBearerManager: %s", str(e))
            raise e
        except Exception as e:
            logger.error("Error in JWTBearerManager: %s", str(e))
            raise InvalidTokenException(
                status_code=HTTP_403_FORBIDDEN,
                detail="JWK-invalid",
            )

        if credentials:
            # TODO: use a constant for the string "Bearer"
            if credentials.scheme != "Bearer":
                logger.error("Error in JWTBearerManager: Wrong authentication method")
                raise InvalidTokenException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail="Wrong authentication method",
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
                logger.error("Error in JWTBearerManager: JWTError")
                raise InvalidTokenException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail="JWK-invalid",
                )

            if not self.auth_provider.verify_token(jwt_credentials):
                logger.error("Error in JWTBearerManager: token not verified")
                raise InvalidTokenException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail="JWK_invalid",
                )

            return jwt_credentials

        return None