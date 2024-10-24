from enum import Enum

from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from api.helpers.objectid import PydanticObjectId


class CommentParentTypeEnum(Enum):
    post = 'post'
    comment = 'comment'


class CommentIn(BaseModel):
    commented_by: str = Field(max_length=60)
    comment: str = Field(max_length=240)


class CommentOut(CommentIn):
    id: PydanticObjectId = Field(alias="_id", default=PydanticObjectId())
    date: datetime = datetime.now()
    likes: list[str] = Field(default=[])
    reposts: list[str] = Field(default=[])
    comments: list['CommentOut'] = Field(default=[])
    edited: bool = Field(default=False)

    def to_pymongo(self):
        pymongo_dict = {"_id": ObjectId(self.id), **self.dict()}
        pymongo_dict.pop('id')
        return pymongo_dict


class CommentUpdateQuery(BaseModel):
    comment: Optional[str] = Field(default=None, max_length=240)
    like: Optional[str] = Field(default=None)
