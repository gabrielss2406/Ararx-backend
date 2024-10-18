from enum import Enum

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from api.helpers.objectid import PydanticObjectId
from api.models.CommentModels import CommentOut


class PostIn(BaseModel):
    content: str = Field(max_length=240)
    author: str = Field(max_length=60)


class PostOut(PostIn):
    id: PydanticObjectId = Field(alias="_id", default=PydanticObjectId())
    date: datetime = datetime.now()
    likes: list[str]
    reposts: list[str]
    comments: list[CommentOut]


class PostUpdateQuery(BaseModel):
    content: Optional[str] = Field(max_length=240)
    author: Optional[str] = Field(max_length=60)
    likes: Optional[int] = Field(default=0)
    id: Optional[int] = Field(default=1)
    date: Optional[datetime] = datetime.now()


class PostOrderByEnum(Enum):
    id = 'id'
    author = 'author'
    date = 'date'
    likes = 'likes'
