from pydantic import BaseModel, Field
from typing import Optional


class LikeOut(BaseModel):
    liked_by: str = Field(max_length=50)


class LikeIn(LikeOut):
    liked_by: str = Field(max_length=50)
    post_id: int = Field(default=1)


class LikeUpdateQuery(LikeIn):
    liked_by: Optional[str] = Field(max_length=50)
    post_id: Optional[int] = Field(default=1)
