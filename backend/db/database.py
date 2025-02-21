from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.config import Settings

# Create the database engine
engine = create_engine(Settings.sqlite.uri)

metadata = sqlalchemy.MetaData()

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get a database session
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_all_tables():
    from models.user import create_user_table
    from models.article import create_articles_table
    from models.comment import create_comments_table
    
    # Call table creation functions for each model
    create_user_table(engine)
    create_articles_table(engine)
    create_comments_table(engine)