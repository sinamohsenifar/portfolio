from ctypes.wintypes import HACCEL
from fastapi import APIRouter, Depends , status ,HTTPException
from db.models.user.models import User


def get_user(user_id,db):
    user = db.query(User).filter(User.id==user_id).first()
    if user:
        return user
    else:
        return {"status": "user not found"}

def get_users(db):
    users = db.query(User).all()
    return {"users": users}

def create_user(user,db):
    
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
        return new_user
    
def update_user(user_id,user,db):
    db_user = db.query(User).filter(User.id == user_id).first()
    # Update the comment
    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
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
