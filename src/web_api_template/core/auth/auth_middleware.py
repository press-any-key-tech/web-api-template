from typing import Dict

from fastapi import Depends, Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from web_api_template.core.auth.cognito.utils import get_current_user
from web_api_template.core.logging import logger


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Aquí puedes agregar información al objeto `request`
        try:
            request.state.current_user = await get_current_user(request=request)
        except Exception as e:
            logger.error("Error in AuthMiddleware: %s", str(e))

        response = await call_next(request)
        return response
