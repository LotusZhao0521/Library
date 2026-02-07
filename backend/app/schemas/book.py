from datetime import datetime

from pydantic import BaseModel


class BookCreate(BaseModel):
    book_no: str
    title: str
    author: str
    isbn: str | None = None
    publisher: str | None = None


class BookUpdate(BaseModel):
    book_no: str | None = None
    title: str | None = None
    author: str | None = None
    isbn: str | None = None
    publisher: str | None = None


class BookResponse(BaseModel):
    id: int
    book_no: str
    title: str
    author: str
    isbn: str | None = None
    publisher: str | None = None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
