from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class UserIn(BaseModel):
    username: str = Field(max_length=50)
    password: str = Field(max_length=50)
    email: EmailStr = Field(max_length=50)


class UserOut(UserIn):
    bio: str = Field(max_length=240)


class UserUpdateQuery(BaseModel):
    email: Optional[EmailStr] = Field(max_length=50)
    password: Optional[str] = Field(max_length=50)
    nickname: Optional[str] = Field(max_length=50)
    bio: Optional[str] = Field(max_length=240)
    username: Optional[str] = Field(max_length=50)
