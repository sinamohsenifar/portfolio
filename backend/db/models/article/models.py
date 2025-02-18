from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
from db.models.user.models import User

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"))  # Foreign key to the User table
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=None)

    # Define the relationship to the User model
    author = relationship("User", back_populates="articles")

# Function to create the table
def create_articles_table(engine):
    Article.metadata.create_all(bind=engine)