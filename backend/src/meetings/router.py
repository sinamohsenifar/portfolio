from fastapi import APIRouter

meeting_router = APIRouter()

@meeting_router.get("/meeting")
def meeting_page():
    return {"message": "wellcome to meeting page"}