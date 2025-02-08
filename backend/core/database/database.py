from core.config import Settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

sqlite = Settings.sqlite

engine = create_engine(sqlite.uri, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(sqlite.autocommit, sqlite.autoflush, bind=engine)
Base = declarative_base()