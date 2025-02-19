from db.models.article.model import Article
from sqlalchemy.orm import Session , joinedload
from db.models.user.models import User
from fastapi import  Depends, HTTPException, status , APIRouter
from db.models.comment.model import Comment


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