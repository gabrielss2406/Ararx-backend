from typing import Any, Optional

from pydantic import BaseModel, Field


class Message(BaseModel):
    message: str
    details: Optional[Any] = Field(default=None)
