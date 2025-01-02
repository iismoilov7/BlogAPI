from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, insert, func
from app.database.schema import User

async def get_user_by_username(
    db: AsyncSession,
    username: str
):
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalar()

async def update_user(
    db: AsyncSession,
    user_id: str,
    ip: str
):
    stmt = update(User).where(User.user_id == user_id).values(logins=User.logins + 1, last_ip=ip)
    await db.execute(stmt)
    await db.commit()


async def get_user_by_id(
    db: AsyncSession,
    user_id: str
):
    stmt = select(User).where(User.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalar()
