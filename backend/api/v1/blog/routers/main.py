from fastapi import APIRouter
from .routers_article import articles_router
from .routers_comment import comments_router

blog_router = APIRouter(prefix="")

blog_router.include_router(articles_router)
blog_router.include_router(comments_router)