from fastapi import APIRouter

from app.api.v1.endpoints import auth, books, borrow_records, users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(users.router, prefix="/users", tags=["用户管理"])
api_router.include_router(books.router, prefix="/books", tags=["图书管理"])
api_router.include_router(
    borrow_records.router, prefix="/borrow-records", tags=["借阅记录"]
)
