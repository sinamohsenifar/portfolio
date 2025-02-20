from typing import Optional , List
from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime
from .comment import CommentResponse



# Define models using Pydantic v2 for validation
class ArticleBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="The title of the article")
    content: str = Field(..., min_length=10, description="The content of the article")
    published: bool = Field(default=True, description="Whether the article is published")

class ArticleCreate(ArticleBase):
    author_id: int = Field(..., gt=0, description="The ID of the author")

    class Config:
        from_attributes = True
        
class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="The title of the article")
    content: Optional[str] = Field(None, min_length=10, description="The content of the article")
    published: Optional[bool] = Field(None, description="Whether the article is published")

    class Config:
        from_attributes = True
        
class ArticleResponse(ArticleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    comments: List[CommentResponse] = []

    class Config:
        from_attributes = True  # Enable ORM mode (previously `orm_mode`)

class ArticleListResponse(BaseModel):
    articles: List[ArticleBase] = []

    class Config:
        from_attributes = True  # Enable ORM mode (previously `orm_mode`)

# Validators
@field_validator("title")
def validate_title(cls, value: str) -> str:
    if len(value) < 1 or len(value) > 100:
        raise ValueError("Title must be between 1 and 100 characters")
    return value

@field_validator("content")
def validate_content(cls, value: str) -> str:
    if len(value) < 10:
        raise ValueError("Content must be at least 10 characters long")
    return value