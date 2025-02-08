from fastapi import APIRouter , status , Response
from enum import Enum
from typing import Optional
from .dependencies import *

# for multiple options in parameters we uses enum
class ArticleType(str, Enum):
    short = 'short'
    story = 'story'
    howto = 'howto'
    

blog_router = APIRouter()

@blog_router.get("/")
def blog_page():
    return {"message": "wellcome to blog page"}


@blog_router.get("/type/{type}", status_code=404)
def article_with_types(type: ArticleType):
    return {"message": f'article type is, {type}'}


@blog_router.get("/id/{id}", status_code=  status.HTTP_200_OK)
def article_with_id(id: int, response: Response):
    if id < 10:
        return {"message": f'article id is {id}'}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f'article {id} not found'}
    


# this wil return article comments with or without comment id {specific or not}
@blog_router.get("/id/{id}/comments/", response_description="Returns list of article comments")
def article_comments(id: int, valid: bool = True , username: Optional[str] = None, comment_id: Optional[int] = None):
    """retrives comments of article
    
    Keyword arguments:
    - **id** -- the id of article
    - **valid** -- optionaly query parameter.
    - **comment_id** -- the id of specific comment . if None retrieves all article comments
    """
    
    return {
        "article": id,
        "comment": comment_id,
        "valid": valid,
        "username": username
        }

@blog_router.get("/all")
def all_articles(page=1, writer="all", tag: Optional[str] = None):
    return {"message": {
        "writer": writer,
        "page": page
    }}
    
# crud articles
@blog_router.post("/create")
def create_article(article: ArticleModel):
    return article

