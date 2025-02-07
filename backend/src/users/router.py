from fastapi import APIRouter

users_router = APIRouter()

@users_router.get("/")
def users_page():
    return {"message": "wellcome to users page"}