from fastapi import APIRouter

portfolio_router = APIRouter()

@portfolio_router.get("/portfolio")
def portfolio_page():
    return {"message": "wellcome to portfolio page"}