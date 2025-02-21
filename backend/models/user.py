from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base
import bcrypt
from ctypes.wintypes import HACCEL
from fastapi import APIRouter, Depends , status ,HTTPException
from schemas.users import UserEmailSchema, UserSchema, UserVerifySchema

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    # Use a string-based reference for the relationship to avoid circular imports
    articles = relationship("Article", back_populates="author")

    # Relationship to the Comment model
    comments = relationship("Comment", back_populates="user")
    
    @staticmethod
    def hash_password(password: str) -> str:
        # Hash the password using bcrypt
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")

    def verify_password(self, plain_password: str) -> bool:
        # Verify the plain password against the hashed password
        return bcrypt.checkpw(plain_password.encode("utf-8"), self.hashed_password.encode("utf-8"))

# Function to create the table
def create_user_table(engine):
    User.metadata.create_all(bind=engine)



def get_user(user_id,db):
    user = db.query(User).filter(User.id==user_id).first()
    if user:
        return user
    else:
        return {"status": "user not found"}

def get_users(db):
    users = db.query(User).all()
    return users

def create_user(user,db):
    check_username = db.query(User).filter(User.username == user.username).first()
    check_email = db.query(User).filter(User.email == user.email).first()
    if check_username:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail="duplicate username")
    elif check_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail="duplicate email")
    else:
        new_user = User(username=user.username, email=user.email, hashed_password = User.hash_password(user.password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
def update_user(user_id,user,db):
    db_user = db.query(User).filter(User.id == user_id).first()
    check_username = db.query(User).filter(User.username == user.username).first()
    check_email = db.query(User).filter(User.email == user.email).first()
    if check_username:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail="duplicate username")
    elif check_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail="duplicate email")
    else:
        # Update the comment
        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user

def update_email(user_id: int, user: UserEmailSchema, db):
    db_user = db.query(User).filter(User.id == user_id).first()
    check_email = db.query(User).filter(User.email == user.email,User.id != user_id).first()
    
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    elif check_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Duplicate Email")
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(user_id,db):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")


def get_user(username,db):
    db_user = db.query(User).filter(User.username == username).first()
    if db_user:
        return db_user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")