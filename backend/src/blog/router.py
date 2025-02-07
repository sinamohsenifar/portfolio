from fastapi import APIRouter

blog_router = APIRouter()

@blog_router.get("/blog")
def blog_page():
    return {"message": "wellcome to blog page"}