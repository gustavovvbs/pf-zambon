from typing import Optional
from datetime import date
from sqlmodel import Field, SQLModel

class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    author: str
    pages: Optional[int] = None
    publication_date: Optional[date] = None
    price: Optional[float] = None

    def __repr__(self):
        return f"<Book(title='{self.title}', author='{self.author}')>"
