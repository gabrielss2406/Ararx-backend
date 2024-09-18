from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CommentIn(BaseModel):
    commented_by: str = Field(max_length=50)
    comment: str = Field(max_length=240)


class CommentOut(CommentIn):
    date: datetime = datetime.now()
    likes: int = Field(default=0)
    id: int = Field(default=1)


class CommentUpdateQuery(BaseModel):
    commented_by: Optional[str] = Field(max_length=50)
    comment: Optional[str] = Field(max_length=240)
    likes: Optional[int] = Field(default=0)
    id: Optional[int] = Field(default=1)
    date: Optional[datetime] = datetime.now()
