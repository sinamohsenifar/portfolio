from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)  # Ensure title is not nullable
    content = Column(String, nullable=False)  # Ensure content is not nullable
    published = Column(Boolean, default=True)  # Default to published
    created_at = Column(DateTime, default=datetime.utcnow)  # Use the function itself, not its result
    updated_at = Column(DateTime, default=None)  # Optional update timestamp
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Ensure author_id is not nullable

    # Relationship to the User model
    author = relationship("User", back_populates="articles")

    # Relationship to the Comment model
    comments = relationship("Comment", back_populates="article")

# Function to create the table
def create_articles_table(engine):
    Article.metadata.create_all(bind=engine)
    
