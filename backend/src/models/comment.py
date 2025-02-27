from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
from models.article import Article
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)  # The content of the comment
    created_at = Column(DateTime, default=datetime.utcnow)  # Timestamp of comment creation
    updated_at = Column(DateTime, default=None)  # Optional update timestamp

    # Foreign key to the User table (who wrote the comment)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="comments")

    # Foreign key to the Article table (which article the comment belongs to)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    article = relationship("Article", back_populates="comments")

    
    


async def create_comment(article_id: int, comment, db: AsyncSession):
    # Check if the article exists
    result = await db.execute(select(Article).filter(Article.id == article_id))
    db_article = result.scalar_one_or_none()
    if not db_article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )

    # Check if the user exists
    result = await db.execute(select(User).filter(User.id == comment.user_id))
    db_user = result.scalar_one_or_none()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Create the comment
    db_comment = Comment(
        content=comment.content,
        user_id=comment.user_id,
        article_id=article_id
    )
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment


async def update_comment(comment_id: int, comment, db: AsyncSession):
    # Check if the comment exists
    result = await db.execute(select(Comment).filter(Comment.id == comment_id))
    db_comment = result.scalar_one_or_none()
    if not db_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    # Update the comment
    for key, value in comment.model_dump(exclude_unset=True).items():
        setattr(db_comment, key, value)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment

async def delete_comment(comment_id: int, db: AsyncSession):
    result = await db.execute(select(Comment).filter(Comment.id == comment_id))
    db_comment = result.scalar_one_or_none()
    if not db_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    await db.delete(db_comment)
    await db.commit()
    return True