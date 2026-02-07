from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.database import AsyncSessionLocal, Base, engine
from app.models import Book, BorrowRecord, User  # noqa: F401 - register models
from app.services.auth_service import auth_service

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables and initial admin
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as session:
        await auth_service.create_initial_admin(
            session, settings.ADMIN_USERNAME, settings.ADMIN_PASSWORD
        )
        await session.commit()
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title="图书管理系统",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")
