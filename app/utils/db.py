from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.utils.settings import settings


Base = declarative_base()

db_url = settings.DB_CONNECTION
if db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)

engine = create_engine(url=db_url)

LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    session = LocalSession()
    try:
        yield session
    finally:
        session.close()