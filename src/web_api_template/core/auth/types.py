from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

JWK = Dict[str, str]


class JWKSEntraID(BaseModel):
    keys: Optional[Dict[str, Any]] = {}
    timestamp: Optional[int] = None
    usage_counter: Optional[int] = 0


class JWKS(BaseModel):
    keys: Optional[List[JWK]] = []
    timestamp: Optional[int] = None
    usage_counter: Optional[int] = 0


class JWTAuthorizationCredentials(BaseModel):
    jwt_token: str
    header: Dict[str, str]
    claims: Dict[str, Any]
    signature: str
    message: str
