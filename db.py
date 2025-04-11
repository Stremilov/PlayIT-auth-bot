from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import logging


import os
from dotenv import load_dotenv

load_dotenv()

# Для создания БД
DB_PASSWORD = os.getenv("DATABASE_PASSWORD")
DB_HOST = os.getenv("DATABASE_HOST", "localhost")
DB_NAME = os.getenv("DATABASE_NAME", "postgres")
DB_USER = os.getenv("DATABASE_USER", "postgres")
DB_PORT = os.getenv("DATABASE_PORT", "5432")


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def get_db_session() -> SessionLocal:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
