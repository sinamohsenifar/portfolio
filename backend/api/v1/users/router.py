from fastapi import APIRouter, Depends , status
from db.models.user.models import User
from .schemas import User_Schema
from db.models.user.crud import create_user
from db.database import get_db
from sqlalchemy.orm.session import Session


db = get_db()

users_router = APIRouter()

@users_router.get("/")
def users_page():
    return {"message": "wellcome to users page"}


@users_router.post("/create")
def create_user(user: User_Schema,db: Session = Depends(get_db), status_code=status.HTTP_201_CREATED):
    return create_user(user)



@users_router.get("/all")
def get_all_users():
    users = db
    pass