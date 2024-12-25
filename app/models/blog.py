from typing import Literal
from pydantic import BaseModel


class User(BaseModel):
    username: str
    name: str
    picture_url: str
    role: Literal["user", "admin", "owner"]


class CreateArticle(BaseModel):
    preview_url: str
    title_ru: str
    title_en: str
    content_ru: str
    content_en: str
    category_id: int


class Aritcle(BaseModel):
    id: int
    preview_url: str
    title: str
    content: str
    created_at: str
    updated_at: str
    category_name: str
    user: User;

class Articles(BaseModel):
    articles: list[Aritcle]


class CreateCategory(BaseModel):
    name_ru: str
    name_en: str
