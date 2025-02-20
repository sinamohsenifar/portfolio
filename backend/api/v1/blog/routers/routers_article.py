from ast import List
from fastapi import  status , APIRouter , Depends
from api.v1.users.schemas import UserSchema
from db.models.article.crud import get_article , get_articles , create_article , delete_article, update_article
from ..schemas.article import ArticleBase, ArticleCreate, ArticleResponse, ArticleUpdate , ArticleListResponse
from sqlalchemy.orm import Session
from db.database import get_db
from api.v1.auth.oauth2 import get_current_user,oauth2_scheme

articles_router = APIRouter(prefix="/articles")

@articles_router.get("/all")
def all_articles(db : Session = Depends(get_db),response_model= List(ArticleResponse)):
    return get_articles(db)

@articles_router.get("/{article_id}", response_model=ArticleResponse)
def gets_article(article_id: int,db : Session = Depends(get_db),):
    return get_article(article_id,db)

@articles_router.post("/")
def creates_article(article:ArticleCreate,db : Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    return {
        "article": create_article(article,db),
        "current_user": current_user.username
        }

@articles_router.put("/{article_id}", response_model=ArticleResponse)
def updates_article(article_id: int, article: ArticleUpdate,db : Session = Depends(get_db),):
    return update_article(article_id , article,db)

@articles_router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletes_article(article_id: int,db : Session = Depends(get_db),):
    return delete_article(db)