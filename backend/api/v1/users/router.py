from fastapi import APIRouter, Depends , status , Response , HTTPException
from db.models.user.crud import create_user, get_user, get_users, update_email , update_user , delete_user
from db.models.user.models import User
from .schemas import UserEmailSchema, UserSchema, UserVerifySchema
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

@users_router.put("/{user_id}/update/user")
def updates_user(user_id: int,user: UserSchema,db: Session = Depends(get_db), status_code=status.HTTP_201_CREATED):
    return update_user(user_id,user,db)

@users_router.put("/{user_id}/update/email")
def updates_user_email(user_id: int,user: UserEmailSchema,db: Session = Depends(get_db), status_code=status.HTTP_201_CREATED):
    return update_email(user_id,user,db)



@users_router.delete("/{user_id}")
def deletes_user(user_id: int,db: Session = Depends(get_db), status_code=status.HTTP_201_CREATED):
    return delete_user(user_id,db)

@users_router.post("/verify")
def verify_password(user: UserVerifySchema,db: Session = Depends(get_db), status_code=status.HTTP_202_ACCEPTED):
    user_found = db.query(User).filter(User.username == user.username).first()
    if user_found:        
        is_valid = user_found.verify_password(user.password)
        if is_valid:
            return {"detail": "correct password"}
        else: 
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="wrong password")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")