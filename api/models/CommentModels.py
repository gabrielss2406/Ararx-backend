from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from api.helpers.objectid import PydanticObjectId


class CommentIn(BaseModel):
    commented_by: str = Field(max_length=60)
    comment: Optional[str] = None


class CommentOut(CommentIn):
    id: PydanticObjectId = Field(alias="_id", default=PydanticObjectId())
    date: datetime = datetime.now()
    likes: list[str] = Field(default=[])
    reposts: list[str] = Field(default=[])
    comments: list["CommentOut"] = Field(default=[])


class CommentUpdateQuery(BaseModel):
    commented_by: Optional[str] = Field(max_length=60)
    comment: Optional[str] = Field(max_length=240)
    likes: Optional[int] = Field(default=0)
    id: Optional[int] = Field(default=1)
    date: Optional[datetime] = datetime.now()
