from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from api.models.LikesModels import LikeOut

class PostOut(BaseModel):
    content: str = Field(max_length=240)
    date = datetime.now()
    likes = [LikeOut]
    id = int = Field(default=1)
    author = str = Field(max_length=50)
    
class PostIn(PostOut):
    content: str = Field(max_length=240)
    author = str = Field(max_length=50)
    
class PostUpdateQuery(PostIn):
    content = Optional[str] = Field(max_length=240)
    author = Optional[str] = Field(max_length=50)
    likes = Optional[int] = Field(default=0)
    id = Optional[int] = Field(default=1)
    date = Optional[datetime] = datetime.now()