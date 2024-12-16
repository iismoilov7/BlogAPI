from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, insert
from app.database.schema import User

async def get_user_by_username(
    db: AsyncSession,
    username: str
):
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalar()
