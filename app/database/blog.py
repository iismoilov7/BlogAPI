from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update
from app.database.schema import Blog, Categories

async def get_article_by_id(db: AsyncSession, id: str):
    stmt = select(Blog).where(Blog.id == id)
    result = await db.execute(stmt)
    return result.scalar()


async def create_article_by_id(
    db: AsyncSession,
    preview_url: str,
    title_ru: str,
    title_en: str,
    content_ru: str,
    content_en: str,
    category_id: int,
    user_id: str,
):
    stmt = insert(Blog).values(
        preview_url=preview_url,
        title_ru=title_ru,
        title_en=title_en,
        content_ru=content_ru,
        content_en=content_en,
        category_id=category_id,
        user_id=user_id,
    )
    await db.execute(stmt)
    await db.commit()


async def get_latest_articles(db: AsyncSession, offset: int, count: int):
    stmt = select(Blog).order_by(Blog.created_at.desc()).offset(offset).limit(count)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_category_by_id(db: AsyncSession, id: str):
    stmt = select(Categories).where(Categories.id == id)
    result = await db.execute(stmt)
    
    # Use first() to get the first result or None if not found
    category = result.scalars().first()  # This will return the actual Categories object or None
    
    return category


async def create_category(db: AsyncSession, name_ru: str, name_en: str):
    stmt = insert(Categories).values(name_ru=name_ru, name_en=name_en).returning(Categories.id)    
    result = await db.execute(stmt)    
    await db.commit()
    category_id = result.scalar()
    return category_id


async def update_category_articles(db: AsyncSession, id: int):
    stmt = update(Categories).where(Categories.id == id).values(articles_length=Categories.articles_length + 1)
    await db.execute(stmt)    
    await db.commit()
