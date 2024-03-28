import base64
import hashlib
import hmac
from datetime import datetime
from time import time, time_ns
from typing import List, Optional

# from botocore.exceptions import ClientError
import requests
from jose import jwk
from jose.utils import base64url_decode

from web_api_template.core.auth.jwt_auth_provider import JWTAuthProvider
from web_api_template.core.auth.user import User
from web_api_template.core.logging import logger

from ...types import JWK, JWKS, JWTAuthorizationCredentials
from .aws_exception import AWSException
from .settings import settings


class CognitoProvider(JWTAuthProvider):

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(CognitoProvider, cls).__new__(cls)
        return cls.instance

    def load_jwks(
        self,
    ) -> JWKS:
        """Load JWKS credentials from remote Identity Provider

        Returns:
            JWKS: _description_
        """

        # TODO: Control errors
        keys: List[JWK] = requests.get(
            settings.AWS_COGNITO_JWKS_URL_TEMPLATE.format(
                settings.AWS_COGNITO_USER_POOL_REGION,
                settings.AWS_COGNITO_USER_POOL_ID,
            )
        ).json()["keys"]
        timestamp: int = (
            time_ns() + settings.AUTH_JWKS_CACHE_INTERVAL_MINUTES * 60 * 1000000000
        )
        usage_counter: int = settings.AUTH_JWKS_CACHE_USAGES
        jks: JWKS = JWKS(keys=keys, timestamp=timestamp, usage_counter=usage_counter)

        return jks

    def verify_token(self, token: JWTAuthorizationCredentials) -> bool:

        hmac_key_candidate = self._get_hmac_key(token)

        if not hmac_key_candidate:
            logger.error(
                "No public key found that matches the one present in the TOKEN!"
            )
            raise AWSException("No public key found!")

        hmac_key = jwk.construct(hmac_key_candidate)

        decoded_signature = base64url_decode(token.signature.encode())

        # if crypto is OK, then check expiry date
        if hmac_key.verify(token.message.encode(), decoded_signature):
            return token.claims["exp"] > time()

        return False

    def create_user_from_token(self, token: JWTAuthorizationCredentials) -> User:
        """Initializes a domain User object with data recovered from a JWT TOKEN.
        Args:
        token (JWTAuthorizationCredentials): Defaults to Depends(oauth2_scheme).

        Returns:
            User: Domain object.

        """

        name_property: str = (
            "username" if "username" in token.claims else "cognito:username"
        )

        return User(
            id=token.claims["sub"],
            name=(
                token.claims[name_property]
                if name_property in token.claims
                else token.claims["sub"]
            ),
            groups=(
                token.claims["cognito:groups"]
                if "cognito:groups" in token.claims
                else [str(token.claims["scope"]).split("/")[-1]]
            ),
            email=token.claims["email"] if "email" in token.claims else None,
        )