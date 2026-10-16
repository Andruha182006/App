from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from schemas.tokens import Token
from schemas.users import UserCreate, UserResponse
from services.users import user_service

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    return await user_service.register_user(db, user_in)

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    token = await user_service.authenticate_user(
        db,
        email=form_data.username,
        password=form_data.password
    )
    return {"access_token": token, "token_type": "bearer"}