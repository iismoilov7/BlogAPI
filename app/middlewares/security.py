from fastapi import Request, HTTPException, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import get_db
from app.database.auth import get_user_by_id
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import ADMIN_URL
from loguru import logger

class AdminAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Check if the request path starts with the admin URL
        if request.url.path.startswith(ADMIN_URL):
            # Get the access token from the request
            try:
                access_token = await request.app.state.security.get_access_token_from_request(request)
                
                # Verify the token
                data = request.app.state.security.verify_token(access_token, verify_csrf=False)

                # Get the database session
                async for db in get_db():  # Ensure you have a valid session
                    user = await get_user_by_id(db, data.sub)

                # Check user role
                if user.role != "owner":
                    raise HTTPException(status_code=403, detail="Forbidden")

                # Process the request
                response = await call_next(request)
                return response
            except Exception as e:
                logger.error(e)
                response = Response(status_code=403, content="Unauthorized")
                response.delete_cookie(key="access_token")
                return response

        # If the request is not for the admin URL, just process it normally
        response = await call_next(request)
        return response
        