from fastapi import APIRouter, Request, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.database.auth import get_user_by_username, update_user, get_user_by_id
from app.models.auth import LoginCreadentials, UserInfo
from app.database.db import get_db
from app.utils.security import check_password

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
        access_token = request.app.state.security.create_access_token(current_user.user_id)
        response.set_cookie(key="access_token", value=access_token)
        
        await update_user(db, current_user.user_id, request.client.host)
        
        return UserInfo(
                username=current_user.username,
                name=current_user.name,
                picture_url=current_user.picture_url,
                role=current_user.role
            )
    else:
        raise HTTPException(403, "Invalid credentials")



@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logout successful"}


@router.get("/me")
async def me(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db)):
    
    access_token = await request.app.state.security.get_access_token_from_request(request)
    
    if access_token is None:
        raise HTTPException(401, "Unauthorized")
    
    try:
        data = request.app.state.security.verify_token(access_token, verify_csrf=False)
        user = await get_user_by_id(db, data.sub)

        return UserInfo(
            username=user.username,
            name=user.name,
            picture_url=user.picture_url,
            role=user.role)
    except Exception as e:
        logger.error(e)
        response.delete_cookie(key="access_token")
        raise HTTPException(403, "Invalid token")
