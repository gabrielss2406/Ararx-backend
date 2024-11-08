from enum import Enum

from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from api.helpers.objectid import PydanticObjectId


class CommentParentTypeEnum(Enum):
    post = "post"
    comment = "comment"


class CommentIn(BaseModel):
    content: str = Field(max_length=240)


class CommentOut(CommentIn):
    id: PydanticObjectId = Field(alias="_id", default=PydanticObjectId())
    commented_by: str = Field(max_length=60)
    date: datetime = datetime.now()
    likes: list[str] = Field(default=[])
    reposts: list[str] = Field(default=[])
    comments: list["CommentOut"] = Field(default=[])
    edited: bool = Field(default=False)

    def to_pymongo(self):
        pymongo_dict = {"_id": ObjectId(self.id), **self.dict()}
        pymongo_dict.pop("id")
        return pymongo_dict


class CommentUpdateQuery(BaseModel):
    new_comment: Optional[str] = Field(default=None, max_length=240)
    add_or_remove_like: Optional[str] = Field(default=None)


class CommentOrderByEnum(Enum):
    id: str = "_id"
    date: str = "date"
    likes: str = "likes"
    reposts: str = "reposts"


class CommentQueryParams(BaseModel):
    page_num: Optional[int] = Field(gt=0, default=1)
    page_size: Optional[int] = Field(gt=0, default=10)
    order_by: Optional[CommentOrderByEnum] = Field(default=CommentOrderByEnum.date)
    desc: Optional[bool] = Field(default=False)
