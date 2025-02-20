
from fastapi import  Depends, HTTPException, status 
from api.v1.blog.schemas.article import ArticleCreate, ArticleUpdate
from db.models.article.model import Article
from db.database import get_db
from sqlalchemy.orm import Session , joinedload


def get_articles(db):
    articles = db.query(Article).all()
    if not articles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no Articles")
    return articles

def get_article(article_id: int, db: Session):
    db_article = db.query(Article).options(joinedload(Article.comments)).filter(Article.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    return db_article

def create_article(article: ArticleCreate, db: Session):
    new_article = Article(
        title=article.title,
        content=article.content,
        author_id=article.author_id  # Ensure author_id is provided
    )
    check_title = db.query(Article).filter(Article.title == new_article.title).first()
    if check_title:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Article title exists")
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

def update_article(article_id: int,article: ArticleUpdate , db: Session):
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    for key, value in db_article.model_dump(exclude_unset=True).items():
        setattr(db_article, key, value)
    db.commit()
    db.refresh(db_article)

    return db_article

def delete_article(article_id: int, db: Session):
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    db.delete(db_article)
    db.commit()
    return ""