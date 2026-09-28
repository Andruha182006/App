from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.tokens import Token
from schemas.users import UserCreate, UserResponse
from services.users import user_service

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Реєстрація нового користувача."""
    return user_service.register_user(db, user_in)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Авторизація користувача та отримання JWT-токена.
    OAuth2PasswordRequestForm очікує поля 'username' (туди передаємо email) та 'password'.
    """
    token = user_service.authenticate_user(
        db,
        email=form_data.username,
        password=form_data.password
    )
    return {"access_token": token, "token_type": "bearer"}