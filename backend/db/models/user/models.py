from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base
import bcrypt

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