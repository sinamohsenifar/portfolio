from fastapi import APIRouter

consoltation_router = APIRouter()

@consoltation_router.get("/consoltation")
def consoltation_page():
    return {"message": "wellcome to consoltation page"}