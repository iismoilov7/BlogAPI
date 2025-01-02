from fastapi import APIRouter, Request, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.database.auth import get_user_by_username, update_user
from app.models.auth import LoginCreadentials, UserInfo, TokenInfo
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
        await update_user(db, current_user.user_id, request.client.host)
        
        return TokenInfo(
            access_token=access_token,
            user=UserInfo(
                username=current_user.username,
                name=current_user.name,
                picture_url=current_user.picture_url,
                role=current_user.role
            )
        )
    else:
        raise HTTPException(403, "Invalid credentials")
