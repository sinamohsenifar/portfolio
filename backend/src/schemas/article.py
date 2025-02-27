from typing import Optional , List
from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime
from .comment import CommentResponse
from pydantic import ConfigDict


class ArticleBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="The title of the article")
    content: str = Field(..., min_length=10, description="The content of the article")
    published: bool = Field(default=True, description="Whether the article is published")

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



class ArticleCreate(ArticleBase):
    author_id: int = Field(..., gt=0, description="The ID of the author")

    model_config = ConfigDict(from_attributes=True)
        
class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="The title of the article")
    content: Optional[str] = Field(None, min_length=10, description="The content of the article")
    published: Optional[bool] = Field(None, description="Whether the article is published")

    model_config = ConfigDict(from_attributes=True)
        
class ArticleResponse(ArticleBase):
    id: int = Field(..., description="The unique ID of the article")
    created_at: datetime = Field(..., description="The timestamp when the article was created")
    updated_at: Optional[datetime] = Field(None, description="The timestamp when the article was last updated")
    comments: list[CommentResponse] = Field(default=[], description="List of comments on the article")

    model_config = ConfigDict(from_attributes=True)

class ArticleListResponse(BaseModel):
    articles: list[ArticleResponse] = Field(default=[], description="List of articles")

    model_config = ConfigDict(from_attributes=True)
