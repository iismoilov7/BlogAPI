from starlette.routing import Match
from fastapi import Request, HTTPException


async def csrf_protection(request: Request, call_next):
    if request.method in ["POST", "PUT", "DELETE"] and request.url.path != "/login":
        csrf_token = request.cookies.get("csrf_token")
        if not csrf_token:
            raise HTTPException(status_code=403, detail="Missing CSRF token in cookies")
    response = await call_next(request)
    return response
