from typing import Literal
from pydantic import BaseModel

class LoginCreadentials(BaseModel):
    username: str
    password: str 


class TokenInfo(BaseModel):
    access_token: str


class UserInfo(BaseModel):
    username: str
    name: str
    picture_url: str
    role: Literal["user", "admin", "owner"]
