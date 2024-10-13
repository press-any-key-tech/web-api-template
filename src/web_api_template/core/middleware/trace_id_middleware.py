from fastapi import FastAPI, Request
from ksuid import Ksuid
from starlette.middleware.base import BaseHTTPMiddleware

from web_api_template.core.logging import trace_id_context

app = FastAPI()


class TraceIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Generar un UUID como trace_id
        trace_id = str(Ksuid())
        # Asignar el trace_id al contexto
        trace_id_context.set(trace_id)

        # Continuar con el manejo de la solicitud
        response = await call_next(request)

        # Limpiar el contexto al finalizar la solicitud
        trace_id_context.set(None)

        return response
