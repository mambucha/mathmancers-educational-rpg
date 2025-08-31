from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Зв'язок з характеристиками гравця
    stats = relationship("PlayerStats", back_populates="owner", uselist=False)

# Нова модель для характеристик гравця
class PlayerStats(Base):
    __tablename__ = "player_stats"

    id = Column(Integer, primary_key=True, index=True)
    hp = Column(Integer, default=100)
    max_hp = Column(Integer, default=100)
    level = Column(Integer, default=1)
    xp = Column(Integer, default=0)
    math_power = Column(Integer, default=10) # <-- ОСЬ ЦЕЙ ВАЖЛИВИЙ РЯДОК

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="stats")

# Нова модель для ворогів
class Enemy(Base):
    __tablename__ = "enemies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    max_hp = Column(Integer, nullable=False)
    math_topic = Column(String, default="addition")
    image_url = Column(String, nullable=True)
    # START: НОВІ ПОЛЯ
    vulnerability = Column(String, nullable=True) # Вразливість
    resistance = Column(String, nullable=True)  # Опір
    # END: НОВІ ПОЛЯ