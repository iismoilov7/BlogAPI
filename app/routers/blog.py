from fastapi import APIRouter, Request, Depends, Response, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from loguru import logger

from app.database.db import get_db
from app.database.blog import (
    get_article_by_id,
    create_article_by_id,
    get_latest_articles,
    get_category_by_id,
    create_category,
    update_category_articles,
    get_categories
)
from app.database.auth import get_user_by_id
from app.models.blog import CreateArticle, Aritcle, User, Articles, CreateCategory

router = APIRouter()


@router.get("/blog/{article_id}")
async def getArticle(
    article_id: int,
    lng: str = Query(default="en"),
    db: AsyncSession = Depends(get_db),
):

    # Get article
    article = await get_article_by_id(db, article_id)

    if article is None:
        raise HTTPException(404, "Article not found")

    # Get user
    user = await get_user_by_id(db, article.user_id)

    # Get category name by id
    category = await get_category_by_id(db, article.category_id)

    if not category:
        raise HTTPException(404, "Category not found")
    
    # Set up article language
    title = article.title_ru if lng == "ru" else article.title_en
    content = article.content_ru if lng == "ru" else article.content_en
    category_name = category.name_ru if lng == "ru" else category.name_en

    
    article_response = Aritcle(
        id=article.id,
        preview_url=article.preview_url,
        title=title,
        content=content,
        created_at=article.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        updated_at=article.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        category_name=category_name,
        user=User(
            username=user.username,
            name=user.name,
            picture_url=user.picture_url,
            role=user.role,
        ),
    )

    return article_response


@router.post("/blog/article/create")
async def createArticle(
    request: Request,
    response: Response,
    article: CreateArticle,
    db: AsyncSession = Depends(get_db),
):
    try:
        access_token = await request.app.state.security.get_access_token_from_request(
            request
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(403, "Invalid token")

    if access_token is None:
        raise HTTPException(401, "Unauthorized")

    try:
        data = request.app.state.security.verify_token(access_token, verify_csrf=False)
        user = await get_user_by_id(db, data.sub)
        is_published = False

        if user.role != "admin" and user.role != "owner":
            raise HTTPException(403, "Forbidden")

        if user.role == "owner":
            is_published = True
        
        
    except Exception as e:
        logger.error(e)
        response.delete_cookie(key="access_token")
        raise HTTPException(403, "Invalid token")

    try:
        await create_article_by_id(
            db,
            article.preview_url,
            article.title_ru,
            article.title_en,
            article.content_ru,
            article.content_en,
            article.category_id,
            data.sub,
            is_published
        )
        
        await update_category_articles(db, article.category_id)
    except IntegrityError:
        return HTTPException(404, "Category not found")

    return {"detail": "Article created"}


@router.get("/blog")
async def getArticles(
    lng: str = Query(default="en"),
    offset: int = Query(default=0, ge=0),
    count: int = Query(default=10, ge=0),
    db: AsyncSession = Depends(get_db),
):

    articles = await get_latest_articles(db, offset, count)

    if not articles:
        raise HTTPException(404, "Articles not found")

    articles_response = Articles(articles=[])

    for article in articles:
        user = await get_user_by_id(db, article.user_id)
        # Get category name by id
        category = await get_category_by_id(db, article.category_id)
        
        if not category:
            raise HTTPException(404, "Category not found")
    
        title = article.title_ru if lng == "ru" else article.title_en
        content = article.content_ru if lng == "ru" else article.content_en
        category_name = category.name_ru if lng == "ru" else category.name_en
        
        article_response = Aritcle(
            id=article.id,
            preview_url=article.preview_url,
            title=title,
            content=content[:100]+"...",
            created_at=article.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            updated_at=article.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            category_name=category_name,
            user=User(
                username=user.username,
                name=user.name,
                picture_url=user.picture_url,
                role=user.role,
            ),
        )

        articles_response.articles.append(article_response)

    return articles_response


# @router.post("/blog/delete/{article_id}")
# async def delete_article(
#     article_id: int,
#     response: Response,
#     db: AsyncSession = Depends(get_db),
# ):
# )


@router.post("/blog/category/add")
async def addCategory(
    request: Request,
    response: Response,
    category_data: CreateCategory,
    db: AsyncSession = Depends(get_db),
):
    try:
        access_token = await request.app.state.security.get_access_token_from_request(
            request
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(403, "Invalid token")

    if access_token is None:
        raise HTTPException(401, "Unauthorized")

    try:
        data = request.app.state.security.verify_token(access_token, verify_csrf=False)
        user = await get_user_by_id(db, data.sub)

        if user.role != "owner":
            raise HTTPException(403, "Forbidden")

        category_id = await create_category(db, category_data.name_ru, category_data.name_en)
        return {
            "category_id": category_id
            }
    except Exception as e:
        logger.error(e)
        response.delete_cookie(key="access_token")
        raise HTTPException(403, "Invalid token")


@router.get("/blog/category/get")
async def getCategories(
    request: Request,
    response: Response,
    lng: str = Query(default="en"),
    db: AsyncSession = Depends(get_db),
):
    
    try:
        access_token = await request.app.state.security.get_access_token_from_request(
            request
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(403, "Invalid token")
    
    if access_token is None:
        raise HTTPException(401, "Unauthorized")

    try:
        data = request.app.state.security.verify_token(access_token, verify_csrf=False)

        categories = await get_categories(db)
        return [{"name": category.name_ru if lng == "ru" else category.name_en, "id": category.id} for category in categories]
    except Exception as e:
        logger.error(e)
        response.delete_cookie(key="access_token")
        raise HTTPException(403, "Invalid token")
