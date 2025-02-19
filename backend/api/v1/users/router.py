from fastapi import APIRouter, Depends , status
from db.models.user.crud import create_user, get_user, get_users , update_user , delete_user
from db.models.user.models import User
from .schemas import UserSchema, UserVerifySchema
from db.database import get_db
from sqlalchemy.orm.session import Session


users_router = APIRouter()

@users_router.get("/{user_id}")
def gets_user(user_id: int, db: Session = Depends(get_db), status_code = status.HTTP_200_OK):
    return get_user(user_id,db)

@users_router.post("/all")
def gets_users(db: Session = Depends(get_db), status_code = status.HTTP_200_OK):
    return get_users(db)

@users_router.post("/create")
def creates_user(user: UserSchema,db: Session = Depends(get_db), status_code=status.HTTP_201_CREATED):
    return create_user(user,db)

@users_router.put("/{user_id}")
def updates_user(user_id: int,user: UserSchema,db: Session = Depends(get_db), status_code=status.HTTP_201_CREATED):
    return update_user(user_id,user,db)

@users_router.delete("/{user_id}")
def deletes_user(user_id: int,db: Session = Depends(get_db), status_code=status.HTTP_201_CREATED):
    return delete_user(user_id,db)

@users_router.post("/verify")
def verify_password(user: UserVerifySchema,db: Session = Depends(get_db), status_code=status.HTTP_202_ACCEPTED):
    user_found = db.query(User).filter(User.username == user.username).first()
    if user_found:        
        is_valid = user_found.verify_password(user.password)
        if is_valid:
            return {"status": "correct password"}
        else: 
            return {"status": "wrong password"}
    else:
        return {"status": "user not found"}