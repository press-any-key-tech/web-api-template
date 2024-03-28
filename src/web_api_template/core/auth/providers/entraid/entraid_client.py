import base64
import hashlib
import hmac
from datetime import datetime
from time import time, time_ns
from typing import List, Optional

import requests
from jose import JWTError, jwk, jwt
from jose.utils import base64url_decode

from web_api_template.core.logging import logger

from ...types import JWK, JWKS, JWTAuthorizationCredentials
from .azure_exception import AzureException
from .settings import settings


class EntraIDClient:

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(EntraIDClient, cls).__new__(cls)
        return cls.instance

    def __get_jwks(self) -> JWKS | None:
        """
        Returns a structure that caches the public keys used by Entra ID to sign its JWT tokens.
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
                openid_config = requests.get(
                    settings.AZURE_ENTRA_ID_JWKS_URL_TEMPLATE.format(
                        settings.AZURE_ENTRA_ID_TENANT_ID,
                    )
                ).json()
                jwks_uri = openid_config["jwks_uri"]
                keys = requests.get(jwks_uri).json()["keys"]

                # Convert 'x5c' field in each key from list to string
                for key in keys:
                    if "x5c" in key and isinstance(key["x5c"], list):
                        key["x5c"] = "".join(key["x5c"])

                timestamp: int = (
                    time_ns()
                    + settings.AUTH_JWKS_CACHE_INTERVAL_MINUTES * 60 * 1000000000
                )
                usage_counter: int = settings.AUTH_JWKS_CACHE_USAGES
                self.jks: JWKS = JWKS(
                    keys=keys, timestamp=timestamp, usage_counter=usage_counter
                )
            else:
                if self.jks.usage_counter is not None:
                    self.jks.usage_counter -= 1

        except KeyError:
            return None

        except Exception as e:
            logger.error("Error in EntraIDClient: %s", str(e))
            raise AzureException("Error in EntraIDClient")

        return self.jks

    def __get_hmac_key(self, token: JWTAuthorizationCredentials) -> Optional[JWK]:
        jwks: Optional[JWKS] = self.__get_jwks()
        if jwks is not None and jwks.keys is not None:
            for key in jwks.keys:
                if key["kid"] == token.header["kid"]:
                    return key
        return None

    def verify_token(self, token: JWTAuthorizationCredentials) -> bool:
        """Verifiy token signature

        Args:
            token (JWTAuthorizationCredentials): _description_

        Raises:
            AzureException: _description_

        Returns:
            bool: _description_
        """

        hmac_key_candidate = self.__get_hmac_key(token)

        if not hmac_key_candidate:
            logger.error(
                "No public key found that matches the one present in the TOKEN!"
            )
            raise AzureException("No public key found!")

        # hmac_key = jwk.construct(hmac_key_candidate)

        try:
            rsa_key = {
                "kty": hmac_key_candidate["kty"],
                "kid": hmac_key_candidate["kid"],
                "use": hmac_key_candidate["use"],
                "n": hmac_key_candidate["n"],
                "e": hmac_key_candidate["e"],
            }

            # Decode jwt token
            payload = jwt.decode(
                token.jwt_token,
                rsa_key,
                algorithms=["RS256"],
                audience=settings.AZURE_ENTRA_ID_AUDIENCE_ID,
                options={"verify_at_hash": False},  # Disable at_hash verification
            )
            return False if payload.get("sub") is None else True
        except JWTError as je:
            logger.error("Error in EntraIDClient: %s", str(je))
            return False
        except Exception as e:
            logger.error("Error in JWTBearerManager: %s", str(e))
            raise AzureException("Error in JWTBearerManager")
