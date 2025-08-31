from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Використовуємо SQLite. Файл бази даних буде створений у папці backend
SQLALCHEMY_DATABASE_URL = "sqlite:///./mathmancers.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)