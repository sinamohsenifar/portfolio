from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)  # Ensure title is not nullable
    content = Column(String, nullable=False)  # Ensure content is not nullable
    published = Column(Boolean, default=True)  # Default to published
    created_at = Column(DateTime, default=datetime.utcnow)  # Use the function itself, not its result
    updated_at = Column(DateTime, default=None)  # Optional update timestamp
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Ensure author_id is not nullable

    # Relationship to the User model
    author = relationship("User", back_populates="articles")

    # Relationship to the Comment model
    comments = relationship("Comment", back_populates="article")

    





async def get_articles(db: AsyncSession):
    result = await db.execute(select(Article))
    articles = result.scalars().all()
    if not articles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are no articles")
    return articles

async def get_article(article_id: int, db: AsyncSession):
    result = await db.execute(
        select(Article)
        .options(joinedload(Article.comments))
        .filter(Article.id == article_id)
    )
    db_article = result.scalar_one_or_none()
    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    return db_article


async def create_article(article, db: AsyncSession):
    # Check if the title already exists
    result = await db.execute(select(Article).filter(Article.title == article.title))
    check_title = result.scalar_one_or_none()
    if check_title:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Article title exists")

    # Create the new article
    new_article = Article(
        title=article.title,
        content=article.content,
        author_id=article.author_id
    )
    db.add(new_article)
    await db.commit()
    await db.refresh(new_article)
    return new_article

async def update_article(article_id: int, article, db: AsyncSession):
    result = await db.execute(select(Article).filter(Article.id == article_id))
    db_article = result.scalar_one_or_none()
    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    # Update the article fields
    for key, value in article.model_dump(exclude_unset=True).items():
        setattr(db_article, key, value)
    await db.commit()
    await db.refresh(db_article)
    return db_article

async def delete_article(article_id: int, db: AsyncSession):
    result = await db.execute(select(Article).filter(Article.id == article_id))
    db_article = result.scalar_one_or_none()
    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    await db.delete(db_article)
    await db.commit()
    return {"status": "Article deleted"}