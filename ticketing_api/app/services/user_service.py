from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from passlib.context import CryptContext
from app.entities.user import User
from app.schemas.user_schemas import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    async def create_user(self, user: UserCreate) -> User:
        hashed_password = self.hash_password(user.password)
        db_user = User(
            email=user.email,
            hashed_password=hashed_password,
            full_name=user.full_name
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def get_user_by_email(self, email: str) -> User:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def get_user(self, user_id: int) -> User:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def get_all_users(self) -> list[User]:
        result = await self.db.execute(select(User))
        return result.scalars().all()