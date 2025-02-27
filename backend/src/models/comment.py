from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
from models.article import Article
from sqlalchemy.orm import Session , joinedload
from models.user import User
from fastapi import  Depends, HTTPException, status , APIRouter


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

# Function to create the table
def create_comments_table(engine):
    Comment.metadata.create_all(bind=engine)
    
    


def create_comment(article_id,comment,db):
    # Check if the article exists
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if not db_article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )

    # Check if the user exists
    db_user = db.query(User).filter(User.id == comment.user_id).first()
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
    db.commit()
    db.refresh(db_comment)
    return db_comment

def update_comment(comment_id,comment,db):
    # Check if the comment exists and belongs to the specified article
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not db_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    # Update the comment
    for key, value in comment.model_dump(exclude_unset=True).items():
        setattr(db_comment, key, value)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def delete_comment(comment_id,db):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not db_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    db.delete(db_comment)
    db.commit()
    return True