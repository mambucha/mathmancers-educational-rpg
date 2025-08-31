from pydantic import BaseModel, EmailStr

# Нова базова схема
class UserBase(BaseModel):
    username: str

    class Config:
        from_attributes = True

# Схема для створення нового користувача
class UserCreate(BaseModel):
    username: str  # Додаємо username
    email: EmailStr
    password: str

# Схема для відображення користувача
class User(BaseModel):
    id: int
    username: str  # Додаємо username
    email: EmailStr

    class Config:
        from_attributes = True # Стара назва orm_mode