from fastapi import APIRouter

blog_router = APIRouter()

@blog_router.get("/")
def blog_page():
    return {"message": "wellcome to blog page"}