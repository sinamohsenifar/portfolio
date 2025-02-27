from ast import List
from fastapi import  status , APIRouter , Depends
from schemas.users import UserSchema
from models.article import get_article , get_articles , create_article , delete_article, update_article
from schemas.article import ArticleBase, ArticleCreate, ArticleResponse, ArticleUpdate , ArticleListResponse
from sqlalchemy.orm import Session
from db.database import get_db
from services.oauth2 import get_current_user,oauth2_scheme

articles_router = APIRouter(prefix="/articles")

@articles_router.get("/all")
async def all_articles(db : Session = Depends(get_db),response_model= List(ArticleResponse)):
    return get_articles(db)

@articles_router.get("/{article_id}", response_model=ArticleResponse)
async def gets_article(article_id: int,db : Session = Depends(get_db)):
    return get_article(article_id,db)

@articles_router.post("/")
async def creates_article(article:ArticleBase,db : Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    new_article = ArticleCreate(
        content=article.content,
        title=article.title,
        published=article.published,
        author_id=current_user.id
    )
    new_article = create_article(new_article,db)
    return {
        "article": new_article,
        "current_user": current_user.username
        }

@articles_router.patch("/{article_id}", response_model=ArticleResponse)
async def updates_article(article_id: int, article: ArticleUpdate,db : Session = Depends(get_db),):
    return update_article(article_id , article,db)

@articles_router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletes_article(article_id: int,db : Session = Depends(get_db),):
    return delete_article(db)