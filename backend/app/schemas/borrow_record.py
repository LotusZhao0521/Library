from datetime import datetime

from pydantic import BaseModel

from app.schemas.book import BookResponse
from app.schemas.user import UserResponse


class BorrowRecordResponse(BaseModel):
    id: int
    book_id: int
    user_id: int
    borrow_time: datetime
    return_time: datetime | None = None
    note: str | None = None
    book: BookResponse
    user: UserResponse

    model_config = {"from_attributes": True}


class NoteUpdate(BaseModel):
    note: str
