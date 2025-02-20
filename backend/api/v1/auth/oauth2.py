from fastapi import Depends, HTTPException , status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from db.models.user.crud import get_user
from db.models.user.models import User
from db.database import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


#openssl-3 rand -hex 64
#   9935510cea28311b7b18df5b71c1d98acc55f912a67e6da4d589b4d2a8aaed6535d1bd9c9d739736ae5ff4c9270ab6c4f2189fabe11612e1b5f3c3dee0bf6157

SECRET_KEY = '9935510cea28311b7b18df5b71c1d98acc55f912a67e6da4d589b4d2a8aaed6535d1bd9c9d739736ae5ff4c9270ab6c4f2189fabe11612e1b5f3c3dee0bf6157'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme),db : Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED , 
        detail="Not allow",
        headers={"WWW-Authenticate":"Bearer"})
    
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        username : str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user(username,db)
    if user:
        return user
    raise credentials_exception