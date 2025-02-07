from fastapi import APIRouter

admin_router = APIRouter()

@admin_router.get("/admin")
def admin_page():
    return {"message": "wellcome to admin page"}