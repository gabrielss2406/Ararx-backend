from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

from api.helpers.objectid import PydanticObjectId
from api.models.CommentModels import CommentOut


class PostIn(BaseModel):
    content: str = Field(max_length=240)
    author: Optional[str] = Field(max_length=60)


class PostOut(PostIn):
    id: PydanticObjectId = Field(alias="_id", default=PydanticObjectId())
    date: datetime = Field(
        default_factory=datetime.now
    )  # Usa o default_factory para a data
    likes: List[str] = []  # Array de handlers que curtiram
    reposts: List[str] = []  # Array de handlers que repostaram
    comments: List[CommentOut] = []  # Array de comentários


class PostUpdateQuery(BaseModel):
    content: Optional[str] = Field(max_length=240)
    author: Optional[str] = Field(max_length=60)
    likes: Optional[List[str]] = None  # Agora é uma lista de handlers
    reposts: Optional[List[str]] = None  # Também deve ser uma lista de handlers
    comments: Optional[List[CommentOut]] = None  # Array de comentários
    date: Optional[datetime] = Field(
        default_factory=datetime.now
    )  # Usa o default_factory para a data


class PostOrderByEnum(Enum):
    id = "id"
    author = "author"
    date = "date"
    likes = "likes"
