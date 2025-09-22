from typing import Optional
from sqlmodel import Field, SQLModel


class Movie(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str
    duration: int
    director: str
    dateCadastro: str