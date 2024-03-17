from typing import Dict

from fastapi import Depends, HTTPException, Request, status
from fastapi.security.utils import get_authorization_scheme_param
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from web_api_template.core.auth.cognito.jw_types import JWTAuthorizationCredentials
from web_api_template.core.auth.cognito.jwt_bearer import JWTBearer
from web_api_template.core.auth.cognito.jwt_bearer_manager import JWTBearerManager
from web_api_template.core.auth.cognito.user import User
from web_api_template.core.auth.cognito.user_not_found_exception import (
    UserNotFoundException,
)
from web_api_template.core.logging import logger

oauth2_scheme: JWTBearer = JWTBearer()


class AuthMiddleware(BaseHTTPMiddleware):
    """Authorization middleware for FastAPI
    Adds the current user to the request state.


    Args:
        BaseHTTPMiddleware (_type_): _description_
    """

    def __init__(self, auth_provider: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth_provider = auth_provider

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            request.state.current_user = await self.get_current_user(request=request)
        except Exception as e:
            logger.error("Error in AuthMiddleware: %s", str(e))

        response = await call_next(request)
        return response

    async def get_current_user(self, request: Request) -> User | None:
        """Get current logged in and active user


        Raises:
            HTTPException: _description_

        Returns:
            User: Domain object.
        """

        logger.debug("Get Current Active User ...")

        try:

            if not self.__validate_credentials(request=request):
                logger.debug("There are no credentiasl in the request")
                return None

            token: JWTAuthorizationCredentials = (
                await JWTBearerManager().get_credentials(request=request)
            )

            # Create User object from token
            user: User = (
                self.__create_user_from_token(token=token)
                if token
                else self.__create_synthetic_user()
            )
            logger.debug("Returning %s", user)
            return user
        except UserNotFoundException as unfe:
            logger.exception("Invalid Token %s", str(unfe))
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as e:
            logger.exception("Not controlled exception")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Server error: {str(e)}",
            )

    def __validate_credentials(self, request: Request) -> bool:
        """Validate if credentials exist in the request headers

        Args:
            request (Request): _description_

        Returns:
            bool: _description_
        """
        authorization = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)
        return authorization and scheme and credentials

    def __create_synthetic_user(self) -> User:
        """Create a synthetic user for testing purposes

        Returns:
            User: Domain object.
        """
        return User(
            id="synthetic",
            name="synthetic",
            groups=[],
            email="synthetic@email.com",
        )

    def __create_user_from_token(self, token: JWTAuthorizationCredentials) -> User:
        """Initializes a domain User object with data recovered from a JWT TOKEN.
        Args:
        token (JWTAuthorizationCredentials): Defaults to Depends(oauth2_scheme).

        Returns:
            User: Domain object.

        """

        name_propetry: str = (
            "username" if "username" in token.claims else "cognito:username"
        )

        # TODO: token claims scope is a string but contains a list of groups
        # separated by space. Modify the token claims to include a list of groups
        return User(
            id=token.claims["sub"],
            name=(
                token.claims[name_propetry]
                if name_propetry in token.claims
                else token.claims["sub"]
            ),
            groups=(
                token.claims["cognito:groups"]
                if "cognito:groups" in token.claims
                else [str(token.claims["scope"]).split("/")[-1]]
            ),
            email=token.claims["email"] if "email" in token.claims else None,
        )
