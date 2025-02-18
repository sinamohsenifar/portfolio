from . import models, schemas
from db.database import get_db
from schemas import User

db = get_db()
user = User
def create_user():
    db_user = models.User(username=user.username, email=user.email, hashed_password="fake_hashed_password")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()