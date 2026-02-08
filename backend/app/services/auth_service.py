from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import User
from app.repositories.user_repository import user_repository


class AuthService:
    async def authenticate(
        self, db: AsyncSession, username: str, password: str
    ) -> User | None:
        user = await user_repository.get_by_username(db, username)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    def create_token(self, user_id: int) -> str:
        return create_access_token(data={"sub": str(user_id)})

    async def create_initial_admin(
        self, db: AsyncSession, username: str, password: str
    ) -> None:
        existing = await user_repository.get_by_username(db, username)
        if existing:
            # 如果用户已存在，更新密码以确保配置中的密码生效
            existing.hashed_password = get_password_hash(password)
            existing.role = "admin"  # 确保角色是 admin
            await user_repository.update(db, existing)
            return
        admin = User(
            username=username,
            hashed_password=get_password_hash(password),
            role="admin",
        )
        await user_repository.create(db, admin)


auth_service = AuthService()
