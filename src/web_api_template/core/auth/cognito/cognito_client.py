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

from web_api_template.core.logging import logger

from .aws_exception import AWSException
from .jw_types import JWK, JWKS, JWTAuthorizationCredentials
from .settings import settings

# import boto3
# import botocore


class CognitoClient:
    def __new__(cls):
        """creates a singleton object, if it is not created,
        or else returns the previous singleton object"""
        if not hasattr(cls, "instance"):
            cls.instance = super(CognitoClient, cls).__new__(cls)
        return cls.instance

    # def __init__(self):
    #     self.client = boto3.client(
    #         "cognito-idp", region_name=self._aws_cognito_user_pool_region
    #     )

    def __get_jwks(self) -> JWKS | None:
        """
        Returns a structure that caches the public keys used by cognito to sign its JWT tokens.
        Cache is refreshed after a settable time or number of reads (usages)
        """
        reload_cache = False
        try:
            if (
                not hasattr(self, "jks")
                or self.jks.timestamp is None
                or self.jks.timestamp < time_ns()
                or self.jks.usage_counter is None
                or self.jks.usage_counter <= 0
            ):
                reload_cache = True
        except AttributeError:
            # the first time after application startup, self.jks is NOT defined
            reload_cache = True

        try:
            if reload_cache:
                # TODO: Control errors
                keys: List[JWK] = requests.get(
                    settings.AWS_COGNITO_JWKS_URL_TEMPLATE.format(
                        settings.AWS_COGNITO_USER_POOL_REGION,
                        settings.AWS_COGNITO_USER_POOL_ID,
                    )
                ).json()["keys"]
                timestamp: int = (
                    time_ns()
                    + settings.AWS_COGNITO_JWKS_CACHE_INTERVAL_MINUTES * 60 * 1000000000
                )
                usage_counter: int = settings.AWS_COGNITO_JWKS_CACHE_USAGES
                self.jks: JWKS = JWKS(
                    keys=keys, timestamp=timestamp, usage_counter=usage_counter
                )
            else:
                self.jks.usage_counter = self.jks.usage_counter - 1

        except KeyError:
            return None

        return self.jks

    def __get_hmac_key(self, token: JWTAuthorizationCredentials) -> Optional[JWK]:
        for key in self.__get_jwks().keys:
            if key["kid"] == token.header["kid"]:
                return key

    def verify_token(self, token: JWTAuthorizationCredentials) -> bool:
        hmac_key_candidate = self.__get_hmac_key(token)

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
