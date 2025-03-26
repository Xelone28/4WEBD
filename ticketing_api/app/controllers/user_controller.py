from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.user_schemas import UserCreate, UserRead
from app.services.user_service import UserService
from app.database.database import get_db
from app.security import get_current_user, verify_password, create_access_token
from datetime import timedelta

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/me", response_model=UserRead)
async def get_current_user_info(current_user: UserRead = Depends(get_current_user)):
    """Retrieve the current authenticated user."""
    return current_user

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await UserService.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )
    created_user = await UserService.create_user(db, user)
    return created_user

@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db), current_user: UserRead = Depends(get_current_user)):
    user = await UserService.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

@router.get("/", response_model=List[UserRead])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    users = await UserService.get_all_users(db)
    return users

@router.post("/login", response_model=dict)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """User login (returns JWT token with admin status)."""
    user = await UserService.get_user_by_email_raw(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=timedelta(minutes=60))
    return {"access_token": access_token, "token_type": "bearer"}
