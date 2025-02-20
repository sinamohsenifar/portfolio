from fastapi import APIRouter , Depends, HTTPException , status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from api.v1.auth import oauth2
from db.models.user.models import User
from db.database import get_db
from .schemas import UserLoginSchema , UserLogoutSchema , UserCheckSchema

auth_router = APIRouter()

@auth_router.post("/token")
def get_token(request : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    if not user.verify_password(request.password):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data={"sub": user.username})
    
    return {
        "access_token": access_token,
        "access_type": request.grant_type,
        "user_id": user.id,
        "username": user.username
    }
    
@auth_router.post("/login")
def logins_user(user: UserLoginSchema, db: Session = Depends(get_db)):
    pass

@auth_router.post("/logout")
def logouts_user(user: UserLogoutSchema, db: Session = Depends(get_db)):
    pass

@auth_router.post("/check")
def checks_user(user: UserCheckSchema, db: Session = Depends(get_db)):
    pass
