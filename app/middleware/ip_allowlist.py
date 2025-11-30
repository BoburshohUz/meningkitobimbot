from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import os

class IPAllowlistMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        env = os.getenv("IPAllowlist", "")
        allow = [x.strip() for x in env.split(",") if x.strip()]
        if allow:
            client = request.client.host if request.client else None
            if client not in allow:
                raise HTTPException(403, "IP ruxsat berilmagan")
        return await call_next(request)
