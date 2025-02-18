from fastapi import APIRouter, Depends , status
from db.models.user.models import User
from .schemas import UserSchema, UserVerifySchema
from db.database import get_db
from sqlalchemy.orm.session import Session


users_router = APIRouter()

@users_router.get("/")
def users_page():
    return {"message": "wellcome to users page"}

@users_router.post("/all")
def all_users(db: Session = Depends(get_db), status_code = status.HTTP_200_OK):
    users = db.query(User).all()
    return {"users": users}



@users_router.post("/create")
def create_user(user: UserSchema,db: Session = Depends(get_db), status_code=status.HTTP_201_CREATED):
    
    # .filter(User.email == user.email).first()
    check_username = db.query(User).filter(User.username == user.username).first()
    check_email = db.query(User).filter(User.email == user.email).first()
    if check_username:
        return {"status": "duplicate username"}
    elif check_email:
        return {"status": "duplicate email"}
    else:
        new_user = User(username=user.username, email=user.email, hashed_password = User.hash_password(user.password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"data": {"username": new_user.username , 
                         "email": new_user.email,
                         "status": "created"
                         }
                }
    
    

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