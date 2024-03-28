from typing import List, Optional, Protocol

from fastapi import Request

from .types import JWTAuthorizationCredentials


class JWTBearerManagerProtocol(Protocol):
    async def get_credentials(
        self, request: Request
    ) -> Optional[JWTAuthorizationCredentials]: ...

    def get_groups(self, token: JWTAuthorizationCredentials) -> Optional[List[str]]: ...
