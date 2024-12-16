from fastapi import APIRouter, Request, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.database.auth import get_user_by_username
from app.models.auth import LoginCreadentials, TokenInfo
from app.database.db import get_db
from app.utils.security import check_password, generate_csrf_token

router = APIRouter()


@router.post("/login")
async def login(
    request: Request,
    user: LoginCreadentials,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    current_user = await get_user_by_username(db, user.username)

    if not current_user:
        raise HTTPException(403, "Invalid credentials")

    if check_password(user.password, current_user.password_hash.encode("utf-8")):
        access_token = request.app.state.security.create_access_token(user.username)
        csrf_token = generate_csrf_token()  # Generate a CSRF token
        response.set_cookie(key="csrf_token", value=csrf_token, httponly=True)
        response.set_cookie(key="access_token", value=access_token)
        return TokenInfo(access_token=access_token)
    else:
        raise HTTPException(403, "Invalid credentials")



@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logout successful"}


@router.get("/me")
async def me(
    request: Request,
    db: AsyncSession = Depends(get_db)):
    
    access_token = await request.app.state.security.get_access_token_from_request(request)
    
    if access_token is None:
        raise HTTPException(401, "Unauthorized")
    
    
    try:
        data = request.app.state.security.verify_token(access_token)
        logger.debug(data)
        return {"username": data["sub"]}
    except Exception as e:
        logger.error(e)
        raise HTTPException(403, "Invalid token")
