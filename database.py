import os
from typing import Annotated
from dotenv import load_dotenv
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

load_dotenv()

engine = None


DB_URL = os.getenv("DATABASE_URL")
if not DB_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(
    DB_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=300
)


def create_db_and_tables():
    """ Creates database and tables if they dont yet exist"""
    if engine:
        SQLModel.metadata.create_all(engine)
    else:
        raise ValueError("Engine is not initialized")
    

def get_session():
    """ gets a database session"""
    if engine:
        with Session(engine) as session:
            yield session


SessionDep = Annotated[Session, Depends(get_session)]