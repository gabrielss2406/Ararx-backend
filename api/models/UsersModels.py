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
    user_handler: str = Field(alias="handler")

    @model_validator(mode="before")
    def set_username(cls, values):
        if values.get("username") is None:
            values["username"] = values.get("handler")
        return values

    def to_pymongo(self):
        pymongo_dict = {"_id": ObjectId(self.id), **self.dict()}
        pymongo_dict.pop("id")
        return pymongo_dict


class UserUpdateQuery(BaseModel):
    email: Optional[EmailStr] = Field(max_length=60)
    password: Optional[str] = Field(max_length=60)
    handler: Optional[str] = Field(max_length=60)
    bio: Optional[str] = Field(max_length=240)
    username: Optional[str] = Field(max_length=60)
