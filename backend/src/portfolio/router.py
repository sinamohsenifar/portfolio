from fastapi import APIRouter

portfolio_router = APIRouter()

@portfolio_router.get("/")
def portfolio_page():
    return {"message": "wellcome to portfolio page"}