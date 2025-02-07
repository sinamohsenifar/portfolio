from fastapi import APIRouter

meeting_router = APIRouter()

@meeting_router.get("/")
def meeting_page():
    return {"message": "wellcome to meeting page"}