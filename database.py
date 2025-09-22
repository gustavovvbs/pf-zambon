import os
from typing import Annotated
from dotenv import load_dotenv
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

load_dotenv()

engine = None

ENV = "DEV"

if ENV == "DEV":
    sqlite_file = "database.db"
    sqlite_url = f"sqlite:///{sqlite_file}"

    connect_args = {
        "check_same_thread": False
    }

    engine = create_engine(
        sqlite_url,
        connect_args=connect_args,
        echo=True
    )
elif ENV == "PROD":
    DB_URL = os.getenv("DATABASE_URL")
    engine = create_engine(
        DB_URL,
        echo=True
    )


def create_db_and_tables():
    """ Creates database and tables if they dont yet exist"""
    if engine:
        SQLModel.metadata.create_all(engine)
    else:
        raise ValueError("Engine is not initializaed")
    

def get_session():
    """ gets a database session"""
    if engine:
        with Session(engine) as session:
            yield session


SessionDep = Annotated[Session, Depends(get_session)]