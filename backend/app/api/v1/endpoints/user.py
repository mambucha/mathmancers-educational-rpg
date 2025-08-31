from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import models
from app.schemas import user as user_schema
from app import auth
from app.api.v1 import deps  # <-- ПРАВИЛЬНИЙ ІМПОРТ

router = APIRouter()


@router.post("/users/", response_model=user_schema.User)
def create_user(user: user_schema.UserCreate, db: Session = Depends(deps.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Використовуємо реальне хешування
    hashed_password = auth.get_password_hash(user.password)

    new_user = models.User(
        email=user.email,
        username=user.username, # Додаємо username
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user