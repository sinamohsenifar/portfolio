from fastapi import APIRouter, status, Response, Path, Query, HTTPException , Depends
from enum import Enum
from typing import Optional, List
from .models import ArticleModel , CommentModel



# Enum for article types
class ArticleType(str, Enum):
    short = "short"
    story = "story"
    howto = "howto"

# Initialize the router
blog_router = APIRouter()

# Welcome endpoint
@blog_router.get("/")
def blog_page():
    return {"message": "Welcome to the blog page"}

# Endpoint to filter articles by type
@blog_router.get("/type/{type}", status_code=status.HTTP_200_OK)
def article_with_types(type: ArticleType):
    return {"message": f"Article type is {type}"}

# Endpoint to get an article by ID
@blog_router.get("/id/{id}", status_code=status.HTTP_200_OK)
def article_with_id(id: int = Path(..., ge=1, description="The ID of the article"), response: Response = None):
    if id < 10:
        return {"message": f"Article id is {id}"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Article {id} not found")

# Endpoint to get article comments
@blog_router.get("/id/{id}/comments/", response_description="Returns list of article comments")
def article_comments(
    id: int = Path(..., ge=1, description="The ID of the article"),
    valid: bool = Query(True, description="Filter comments by validity"),
    username: Optional[str] = Query(None, description="Filter comments by username"),
    comment_id: Optional[int] = Query(None, description="The ID of a specific comment"),
    tags: List[str] = Query([], description="Filter comments by tags")
):
    """Retrieves comments of an article.

    Args:
    - **id** (int): The ID of the article.
    - **valid** (bool): Optional query parameter to filter comments by validity. Defaults to True.
    - **username** (Optional[str]): Optional query parameter to filter comments by username.
    - **comment_id** (Optional[int]): Optional query parameter to retrieve a specific comment by its ID.
    - **tags** (List[str]): Optional query parameter to filter comments by tags.

    Returns:
    - dict: A dictionary containing the article ID, comment ID (if provided), validity filter, username filter, and tags.
    """
    return {
        "article_id": id,
        "comment_id": comment_id,
        "valid": valid,
        "username": username,
        "tags": tags
    }

# Endpoint to get all articles with pagination and filters
@blog_router.get("/all")
def all_articles(
    page: int = Query(1, ge=1, description="Page number for pagination"),
    writer: str = Query("all", description="Filter articles by writer"),
    tags: List[str] = Query([], description="Filter articles by tags")
):
    return {
        "message": {
            "writer": writer,
            "page": page,
            "tags": tags
        }
    }

# Endpoint to create a new article
@blog_router.post("/create", status_code=status.HTTP_201_CREATED)
def create_article(article: ArticleModel):
    return article

# Endpoint to create a new comment
@blog_router.post("/comments/create", status_code=status.HTTP_201_CREATED)
def create_comment(comment: CommentModel):
    return comment

# Endpoint to update an article
@blog_router.put("/update/{id}")
def update_article(id: int, article: ArticleModel):
    return {"message": f"Article {id} updated", "article": article}

# Endpoint to delete an article
@blog_router.delete("/delete/{id}")
def delete_article(id: int):
    return {"message": f"Article {id} deleted"}