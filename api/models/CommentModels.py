from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CommentOut(BaseModel):
    commented_by = str = Field(max_length=50)
    date = datetime.now()
    likes = int = Field(default=0)
    id = int = Field(default=1)
    comment = str = Field(max_length=240)
    
class CommentIn(CommentOut):
    commented_by = str = Field(max_length=50)
    comment = str = Field(max_length=240)

class CommentUpdateQuery(CommentIn):
    commented_by = Optional[str] = Field(max_length=50)
    comment = Optional[str] = Field(max_length=240)
    likes = Optional[int] = Field(default=0)
    id = Optional[int] = Field(default=1)
    date = Optional[datetime] = datetime.now()