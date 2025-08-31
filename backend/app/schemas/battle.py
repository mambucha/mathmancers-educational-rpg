from pydantic import BaseModel
from typing import Any, Optional
from .user import UserBase

class Problem(BaseModel):
    display_text: str
    data: dict[str, Any]
    answer: int

class PlayerStats(BaseModel):
    hp: int
    max_hp: int
    level: int
    xp: int
    math_power: int
    combo_meter: int = 0
    max_combo_meter: int = 100
    owner: UserBase
    
    class Config:
        from_attributes = True

class Enemy(BaseModel):
    id: int
    name: str
    max_hp: int
    math_topic: str
    image_url: str | None = None
    vulnerability: str | None = None  # Додаємо нові поля з моделі
    resistance: str | None = None
    
    class Config:
        from_attributes = True

class BattleState(BaseModel):
    player_stats: PlayerStats
    enemy: Enemy
    enemy_current_hp: int
    problem: Problem

class AnswerPayload(BaseModel):
    enemy_id: int
    problem: Problem
    answer: int | None = None
    operation: str | None = None

# Розширена схема результату для додаткової інформації
class AnswerResult(BaseModel):
    is_correct: bool
    new_player_stats: PlayerStats
    xp_gained: int
    damage_dealt: int = 0
    new_problem: Problem | None = None
    
    # Нові поля для навчального фідбеку
    feedback_message: Optional[str] = None
    concept_reinforcement: Optional[str] = None
    mistake_analysis: Optional[str] = None
    encouragement: Optional[str] = None