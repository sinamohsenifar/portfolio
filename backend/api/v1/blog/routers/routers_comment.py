from fastapi import  Depends, HTTPException, status , APIRouter
from sqlalchemy.orm import Session
from db.models.comment.crud import create_comment , update_comment , delete_comment
from db.database import get_db
from db.models.article.model import Article
from ..schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from db.models.comment.model import Comment

comments_router = APIRouter(prefix="")


# Create a new comment for an article
@comments_router.post("/comments/{article_id}", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def creates_comment(article_id: int,comment: CommentCreate,db: Session = Depends(get_db)):
    return create_comment(article_id,comment,db)

# Update a comment
@comments_router.put("/comments/{comment_id}", response_model=CommentResponse)
def updates_comment(comment_id: int,comment: CommentUpdate,db: Session = Depends(get_db)):
    return update_comment(comment_id,comment,db)

# Delete a comment
@comments_router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletes_comment(comment_id: int,db: Session = Depends(get_db)):
    return delete_comment(comment_id,db)