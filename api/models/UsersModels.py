from enum import Enum

from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr, model_validator
from typing import Optional

from api.helpers.objectid import PydanticObjectId


class UserIn(BaseModel):
    handler: str = Field(max_length=60)
    password: str = Field(max_length=60)
    email: EmailStr = Field(max_length=60)


class UserOut(UserIn):
    id: PydanticObjectId = Field(alias="_id", default=PydanticObjectId())
    username: str = Field(max_length=50, default=None)
    bio: str = Field(max_length=240, default="")
    followers: list[str] = Field(default=[])
    following: list[str] = Field(default=[])
    isFollowing: bool = Field(default=False)
    isMe: bool = Field(default=False)

    @model_validator(mode="before")
    def set_username(cls, values):
        if values.get("username") is None:
            values["username"] = values.get("handler")
        return values

    def to_pymongo(self):
        pymongo_dict = {"_id": ObjectId(self.id), **self.dict()}
        pymongo_dict.pop("id")
        return pymongo_dict


class UserOrderByEnum(Enum):
    email: str = "email"
    handler: str = "handler"
    bio: str = "bio"
    username: str = "username"


class UserQueryParams(BaseModel):
    page_num: Optional[int] = Field(gt=0, default=1)
    page_size: Optional[int] = Field(gt=0, default=10)
    order_by: Optional[UserOrderByEnum] = Field(default=UserOrderByEnum.handler)
    desc: Optional[bool] = Field(default=False)


class UserUpdateQuery(BaseModel):
    email: Optional[EmailStr] = Field(max_length=60, default=None)
    handler: Optional[str] = Field(max_length=60, default=None)
    bio: Optional[str] = Field(max_length=240, default=None)
    username: Optional[str] = Field(max_length=60, default=None)
