from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)  # The content of the comment
    created_at = Column(DateTime, default=datetime.utcnow)  # Timestamp of comment creation
    updated_at = Column(DateTime, default=None)  # Optional update timestamp

    # Foreign key to the User table (who wrote the comment)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="comments")

    # Foreign key to the Article table (which article the comment belongs to)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    article = relationship("Article", back_populates="comments")

# Function to create the table
def create_comments_table(engine):
    Comment.metadata.create_all(bind=engine)