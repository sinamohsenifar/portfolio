from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from db.database import get_db
from db.models.article.models import Article
from .schemas import ArticleCreate, ArticleResponse, ArticleUpdate , ArticleListResponse
from db.models.article.models import Comment
from db.models.article.models import Article
from db.models.user.models import User
from .schemas import CommentCreate, CommentUpdate, CommentResponse

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("/all")
def all_articles(db: Session = Depends(get_db), response_model= ArticleListResponse ):
    articles = db.query(Article).all()
    if not articles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no Articles")
    return {"articles": articles}

@router.post("/", response_model=ArticleResponse)
def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    db_article = Article(**article.model_dump())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

@router.get("/{article_id}", response_model=ArticleResponse)
def read_article(article_id: int, db: Session = Depends(get_db)):
    db_article = db.query(Article).options(joinedload(Article.comments)).filter(Article.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    return db_article

@router.put("/{article_id}", response_model=ArticleResponse)
def update_article(article_id: int, article: ArticleUpdate, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    for key, value in article.model_dump(exclude_unset=True).items():
        setattr(db_article, key, value)
    db.commit()
    db.refresh(db_article)
    return db_article

@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(article_id: int, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    db.delete(db_article)
    db.commit()
    

# Create a new comment for an article
@router.post("/{article_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    article_id: int,  # ID of the article to which the comment belongs
    comment: CommentCreate,  # Comment data from the request body
    db: Session = Depends(get_db)  # Database session
):
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

# Update a comment
@router.put("/{article_id}/comments/{comment_id}", response_model=CommentResponse)
def update_comment(
    article_id: int,  # ID of the article to which the comment belongs
    comment_id: int,  # ID of the comment to update
    comment: CommentUpdate,  # Updated comment data from the request body
    db: Session = Depends(get_db)  # Database session
):
    # Check if the comment exists and belongs to the specified article
    db_comment = db.query(Comment).filter(
        Comment.id == comment_id,
        Comment.article_id == article_id
    ).first()
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

# Delete a comment
@router.delete("/{article_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    article_id: int,  # ID of the article to which the comment belongs
    comment_id: int,  # ID of the comment to delete
    db: Session = Depends(get_db)  # Database session
):
    # Check if the comment exists and belongs to the specified article
    db_comment = db.query(Comment).filter(
        Comment.id == comment_id,
        Comment.article_id == article_id
    ).first()
    if not db_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    # Delete the comment
    db.delete(db_comment)
    db.commit()
    return None