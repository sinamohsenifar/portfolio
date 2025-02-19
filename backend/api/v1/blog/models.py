from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime


# Comment Base Schema
class CommentBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=500, description="The content of the comment")
    user_id: int = Field(..., gt=0, description="The ID of the user who wrote the comment")

# Comment Create Schema
class CommentCreate(CommentBase):
    pass  # No additional fields for creation

# Comment Update Schema
class CommentUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1, max_length=500, description="The content of the comment")

# Comment Response Schema
class CommentResponse(CommentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Enable ORM mode (previously `orm_mode`)

# Validators
@field_validator("content")
def validate_content(cls, value: str) -> str:
    if len(value) < 1 or len(value) > 500:
        raise ValueError("Content must be between 1 and 500 characters")
    return value



# Define models using Pydantic v2 for validation
class ArticleBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="The title of the article")
    content: str = Field(..., min_length=10, description="The content of the article")
    published: bool = Field(default=True, description="Whether the article is published")
    author_id: int = Field(..., gt=0, description="The ID of the author")

class ArticleCreate(ArticleBase):
    pass  # No additional fields for creation

class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="The title of the article")
    content: Optional[str] = Field(None, min_length=10, description="The content of the article")
    published: Optional[bool] = Field(None, description="Whether the article is published")

class ArticleResponse(ArticleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    comments: CommentResponse

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