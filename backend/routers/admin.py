from fastapi import APIRouter

admin_router = APIRouter()

@admin_router.get("/")
def admin_page():
    return {"message": "wellcome to admin page"}