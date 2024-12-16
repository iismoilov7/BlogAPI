import asyncio
import uuid

from loguru import logger

from app.database.schema import User
from app.database.db import init_db, get_db
from app.utils.security import hash_password



async def create_user(name, username, password, role):
    password_hash = hash_password(password)

    async for session in get_db():
        user = User(
            user_id=f"{username}_{uuid.uuid4()}",
            name=name,
            username=username,
            password_hash=password_hash.decode('utf-8'),
            role=role
        )
        session.add(user)
        await session.commit()
    logger.info("User created")

async def main():
    await init_db()
    name = input("Set users name: ")
    username = input("Set a username: ")
    password = input("Set a password: ")
    role = input("Set a role (user, admin, owner): ")

    await create_user(name, username, password, role)


if __name__ == "__main__":
    asyncio.run(main())
