from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

DB_PASSWORD = settings.DB_PASSWORD
DB_USER = settings.DB_USER
DB_HOST = settings.DB_HOST
DB_NAME = settings.DB_NAME
SQL_ALCHMEY_URL = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(SQL_ALCHMEY_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
