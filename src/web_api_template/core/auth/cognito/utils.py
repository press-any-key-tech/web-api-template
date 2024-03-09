from typing import Any, Tuple

from fastapi import Depends, HTTPException, status

from web_api_template.core.logging import logger

from .jw_types import JWTAuthorizationCredentials
from .jwt_bearer import JWTBearer
from .settings import settings
from .user import User
from .user_not_found_exception import UserNotFoundException

# oauth2_scheme: JWTBearer = JWTBearer() if not settings.AUTH_DISABLED else None
oauth2_scheme: JWTBearer = JWTBearer()


def get_current_active_user(
    token: JWTAuthorizationCredentials = Depends(oauth2_scheme),
) -> User:
    """Get current logged in and active user

    Args:
        token (str, optional): _description_. Defaults to Depends(oauth2_scheme).

    Raises:
        HTTPException: _description_

    Returns:
        User: Domain object.
    """

    try:
        # Create User object from token
        user: User = (
            __create_user_from_token(token=token)
            if token
            else __create_synthetic_user()
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
    except Exception:
        logger.exception("Not controlled exception")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server error"
        )


def __create_synthetic_user() -> User:
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


def __create_user_from_token(token: JWTAuthorizationCredentials) -> User:
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
            else str(token.claims["scope"]).split("/")[-1]
        ),
        email=token.claims["email"] if "email" in token.claims else None,
    )
