from fastapi import APIRouter

users_router = APIRouter()

@users_router.get("/users")
def users_page():
    return {"message": "wellcome to users page"}