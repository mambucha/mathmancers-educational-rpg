from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import models
from app.schemas import battle as battle_schema # Ми можемо перевикористати схему PlayerStats
from app.auth import get_current_user
from app.api.v1 import deps
from app.schemas import user as user_schema

router = APIRouter()

@router.get("/player/me", response_model=battle_schema.PlayerStats)
def read_player_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Отримати статистику для поточного авторизованого гравця.
    """
    player_stats = (
        db.query(models.PlayerStats)
        .filter(models.PlayerStats.owner_id == current_user.id)
        .first()
    )

    # Якщо гравець зареєструвався, але ще жодного разу не грав,
    # його статистики не існує. Створимо її.
    if not player_stats:
        player_stats = models.PlayerStats(owner_id=current_user.id)
        db.add(player_stats)
        db.commit()
        db.refresh(player_stats)

    return player_stats
@router.post("/player/heal", response_model=battle_schema.PlayerStats)
def heal_player(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Повністю відновлює здоров'я поточного гравця.
    Якщо статистики не існує - створює її.
    """
    player_stats = (
        db.query(models.PlayerStats)
        .filter(models.PlayerStats.owner_id == current_user.id)
        .first()
    )

    # START: ВИПРАВЛЕННЯ
    # Якщо статистики не існує - створюємо її, замість того щоб повертати помилку.
    if not player_stats:
        player_stats = models.PlayerStats(owner_id=current_user.id)
        db.add(player_stats)
        db.commit()
        db.refresh(player_stats)
    # END: ВИПРАВЛЕННЯ

    player_stats.hp = player_stats.max_hp  # Встановлюємо HP на максимум
    db.commit()
    db.refresh(player_stats)
    return player_stats