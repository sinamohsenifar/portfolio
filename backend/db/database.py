from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import Settings

# Create the database engine
engine = create_engine(Settings.sqlite.uri)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def create_all_tables():
    from db.models.user.model import create_table as user_create_table

    # Call table creation functions for each model
    user_create_table(engine)
