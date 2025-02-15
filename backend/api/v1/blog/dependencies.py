from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class ArticleModel(BaseModel):
    title: str
    content: str
    published: bool = True 
    created_at: datetime
    updated_at: Optional[datetime] = None
    author: int

class CommentModel(BaseModel):
    title: str
    user: int
    content: str
    created_at: datetime