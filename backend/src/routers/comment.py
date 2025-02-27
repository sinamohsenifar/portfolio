from fastapi import  Depends, status , APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from models.comment import create_comment , update_comment , delete_comment
from db.database import get_db
from schemas.comment import CommentCreate, CommentUpdate, CommentResponse

comments_router = APIRouter(prefix="")


# Create a new comment for an article
@comments_router.post("/comments/{article_id}", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def creates_comment(article_id: int,comment: CommentCreate,db: AsyncSession = Depends(get_db)):
    return await create_comment(article_id,comment,db)

# Update a comment
@comments_router.put("/comments/{comment_id}", response_model=CommentResponse)
async def updates_comment(comment_id: int,comment: CommentUpdate,db: AsyncSession = Depends(get_db)):
    return await update_comment(comment_id,comment,db)

# Delete a comment
@comments_router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletes_comment(comment_id: int,db: AsyncSession = Depends(get_db)):
    return await delete_comment(comment_id,db)