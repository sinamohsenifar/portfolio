from db.models.user.hash import Hash
from db.models.user.models import User
from db.models.user.schemas import User_Schema
from sqlalchemy.orm.session import Session
from db.database import get_db


def create_user(user: User_Schema, db: Session):
    new_user = User(username=user.username, email=user.email, hashed_password=Hash.bcrypt(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(user_id: int, db: Session):
    return db.query(User).filter(User.id == user_id).first()