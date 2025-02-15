from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime

# Define models using Pydantic v2 for validation
class ArticleModel(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="The title of the article")
    content: str = Field(..., min_length=10, description="The content of the article")
    published: bool = Field(default=True, description="Whether the article is published")
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp of article creation")
    updated_at: Optional[datetime] = Field(None, description="Timestamp of article update")
    author: int = Field(..., gt=0, description="The ID of the author")

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

class CommentModel(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="The title of the comment")
    user: int = Field(..., gt=0, description="The ID of the user")
    content: str = Field(..., min_length=1, description="The content of the comment")
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp of comment creation")

    @field_validator("title")
    def validate_comment_title(cls, value: str) -> str:
        if len(value) < 1 or len(value) > 100:
            raise ValueError("Comment title must be between 1 and 100 characters")
        return value

    @field_validator("content")
    def validate_comment_content(cls, value: str) -> str:
        if len(value) < 1:
            raise ValueError("Comment content must be at least 1 character long")
        return value