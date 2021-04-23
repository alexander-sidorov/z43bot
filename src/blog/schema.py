from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class User(BaseModel):
    id: Optional[int] = Field(None)
    username: str
    password: str


class Post(BaseModel):
    author_id: Optional[int] = Field(None)
    content: Optional[str] = Field(None)
    id: Optional[int] = Field(None)
    image: Optional[str] = Field(None)
    title: Optional[str] = Field(None)
