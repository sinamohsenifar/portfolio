from typing import List
from fastapi import status, APIRouter, Depends, HTTPException
from schemas.users import UserBase
from models.article import get_article, get_articles, create_article, delete_article, update_article
from schemas.article import ArticleBase, ArticleCreate, ArticleResponse, ArticleUpdate, ArticleListResponse
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from services.oauth2 import get_current_user

articles_router = APIRouter(prefix="/articles", tags=["articles"])

# Get all articles
@articles_router.get("/all", response_model=ArticleListResponse)
async def all_articles(db: AsyncSession = Depends(get_db)):
    articles = await get_articles(db)
    return {"articles": articles}

# Get a single article by ID
@articles_router.get("/{article_id}", response_model=ArticleResponse)
async def gets_article(article_id: int, db: AsyncSession = Depends(get_db)):
    article = await get_article(article_id, db)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    return article

# Create a new article
@articles_router.post("/", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
async def creates_article(
    article: ArticleBase,
    db: AsyncSession = Depends(get_db),
    current_user: UserBase = Depends(get_current_user)
):
    new_article = ArticleCreate(
        **article.model_dump(),
        author_id=current_user.id
    )
    created_article = await create_article(new_article, db)
    return created_article

# Update an existing article
@articles_router.patch("/{article_id}", response_model=ArticleResponse)
async def updates_article(
    article_id: int,
    article: ArticleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserBase = Depends(get_current_user)
):
    # Check if the article exists and belongs to the current user
    db_article = await get_article(article_id, db)
    if not db_article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    if db_article.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this article"
        )

    updated_article = await update_article(article_id, article, db)
    return updated_article

# Delete an article
@articles_router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletes_article(
    article_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserBase = Depends(get_current_user)
):
    # Check if the article exists and belongs to the current user
    db_article = await get_article(article_id, db)
    if not db_article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    if db_article.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this article"
        )

    await delete_article(article_id, db)
    return None