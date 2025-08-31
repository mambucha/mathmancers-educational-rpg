from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from app.db import models
from app.schemas import battle as battle_schema
from app.services import math_service
from app.auth import get_current_user
from app.api.v1 import deps
from app.services.math_service import generate_special_encounter

router = APIRouter()

@router.get("/battle/start", response_model=battle_schema.BattleState)
def start_battle(db: Session = Depends(deps.get_db), current_user: models.User = Depends(get_current_user)):
    """Розпочинає бій з випадковим ворогом з підтримкою спеціальних зустрічей"""
    
    # Отримуємо випадкового ворога
    enemy = db.query(models.Enemy).order_by(func.random()).first()
    if not enemy:
        raise HTTPException(status_code=404, detail="No enemies found in database")

    # Отримуємо або створюємо статистики гравця
    player_stats = db.query(models.PlayerStats).filter(models.PlayerStats.owner_id == current_user.id).first()
    if not player_stats:
        player_stats = models.PlayerStats(owner_id=current_user.id)
        db.add(player_stats)
        db.commit()
        db.refresh(player_stats)

    # Перевіряємо, чи це спеціальний ворог
    if enemy.name == "Geometric Gargoyle" or "geometric" in enemy.name.lower():
        problem, encounter_data = generate_special_encounter(enemy.name, player_stats.level)
        
        # Оновлюємо дані ворога з encounter_data якщо потрібно
        enemy.description = encounter_data.get("description", enemy.name)
        
    else:
        # Генеруємо звичайну задачу
        problem = math_service.generate_problem(
            topic=enemy.math_topic, 
            level=player_stats.level,
            player_id=current_user.id
        )

    return battle_schema.BattleState(
        player_stats=player_stats,
        enemy=enemy,
        enemy_current_hp=enemy.max_hp,
        problem=problem
    )


@router.post("/battle/answer", response_model=battle_schema.AnswerResult)
def submit_answer(payload: battle_schema.AnswerPayload, db: Session = Depends(deps.get_db), current_user: models.User = Depends(get_current_user)):
    """Обробляє відповідь гравця з концептуальним фідбеком"""
    
    enemy = db.query(models.Enemy).filter(models.Enemy.id == payload.enemy_id).first()
    player_stats = db.query(models.PlayerStats).filter(models.PlayerStats.owner_id == current_user.id).first()

    if not enemy or not player_stats:
        raise HTTPException(status_code=404, detail="Player or Enemy not found")

    problem = payload.problem
    is_correct = False
    problem_data = problem.data or {}
    problem_type = problem_data.get("type") or enemy.math_topic

    # Визначаємо правильність відповіді
    if problem_type == "progressive_equation" and payload.operation:
        # Нова прогресивна алгебра
        from app.services.math_service import adaptive_engine
        
        response_analysis = adaptive_engine.process_student_response(
            current_user.id,
            problem_data,
            payload.operation
        )
        
        is_correct = response_analysis["is_correct"]
        
        # Оновлюємо problem_data для наступного кроку
        if "next_step" in response_analysis and response_analysis["next_step"] is not None:
            problem_data["current_step"] = response_analysis["next_step"]
            new_problem_obj = problem  # Оновлюємо існуючу задачу
            new_problem_obj.data = problem_data
        elif response_analysis.get("is_equation_solved", False):
            # Генеруємо нову задачу після завершення поточної
            new_problem_obj = math_service.generate_problem(
                topic=enemy.math_topic, 
                level=player_stats.level,
                player_id=current_user.id
            )
        else:
            new_problem_obj = problem  # Повторюємо той самий крок
            new_problem_obj.data = problem_data
            
        # Використовуємо детальний фідбек з адаптивної системи
        feedback_message = response_analysis.get("feedback", "")
        concept_reinforcement = response_analysis.get("mastery_update", {})
        mistake_analysis = response_analysis.get("error_analysis", {}).get("pattern", "")
        encouragement = response_analysis.get("encouragement", "")
        
    elif problem_type == "equation" and payload.operation:
        # Стара система алгебри (fallback)
        steps = problem_data.get("solution_steps", [])
        index = problem_data.get("current_step_index", 0)
        if index < len(steps) and payload.operation.strip() == steps[index].get("operation", "").strip():
            is_correct = True
    elif payload.answer is not None and problem.answer is not None:
        if payload.answer == problem.answer:
            is_correct = True

    # Генеруємо концептуальний фідбек
    feedback_message = ""
    concept_reinforcement = ""
    mistake_analysis = ""
    encouragement = ""

    xp_gained = 0
    damage_dealt = 0
    new_problem_obj = problem

    if is_correct:
        # Розрахунок шкоди з урахуванням vulnerability/resistance
        base_damage = 15 + player_stats.math_power
        if enemy.vulnerability and enemy.vulnerability == problem_type:
            damage_dealt = base_damage * 2
            feedback_message = f"Критичний удар! Ворог слабкий до {problem_type}!"
        elif enemy.resistance and enemy.resistance == problem_type:
            damage_dealt = base_damage // 2
            feedback_message = f"Ворог стійкий до {problem_type}. Спробуйте інший тип задач."
        else:
            damage_dealt = base_damage
            feedback_message = f"Влучний удар! Завдано {damage_dealt} шкоди."

        # Нараховуємо досвід
        xp_gained = 10
        player_stats.xp += xp_gained

        # Перевірка підвищення рівня
        xp_for_next_level = 100 * player_stats.level
        if player_stats.xp >= xp_for_next_level:
            player_stats.level += 1
            player_stats.max_hp += 10
            player_stats.hp = player_stats.max_hp
            player_stats.math_power += 5
            encouragement = f"🌟 Рівень підвищено до {player_stats.level}! Ваша математична сила зросла!"

        # Концептуальне підкріплення
        concept_reinforcement = problem_data.get("concept_hint", "")
        if not concept_reinforcement and problem_data.get("context_explanation"):
            concept_reinforcement = problem_data["context_explanation"]

        # Генеруємо нову задачу
        if problem_type == "equation":
            # Логіка для алгебри (залишаємо без змін)
            problem_data["current_step_index"] += 1
            parts = problem_data.get("equation_parts", {})
            if problem_data["current_step_index"] == 1:
                parts["c"] -= parts["b"]
                parts["b"] = 0
            elif problem_data["current_step_index"] == 2:
                parts["c"] //= parts["a"]
                parts["a"] = 1
                parts["x_isolated"] = True
            
            if parts.get("x_isolated"):
                new_problem_obj = math_service.generate_problem(topic=enemy.math_topic, level=player_stats.level)
            else:
                new_problem_obj.data = problem_data
        else:
            new_problem_obj = math_service.generate_problem(topic=enemy.math_topic, level=player_stats.level)

    else:
        # Неправильна відповідь
        player_damage = 10
        player_stats.hp = max(0, player_stats.hp - player_damage)
        
        feedback_message = f"Неправильно! Ви отримали {player_damage} шкоди."
        
        # Аналіз помилки на основі контексту
        context = problem_data.get("context", "")
        if context == "magic_crystals" and problem_type == "addition":
            mistake_analysis = "Пам'ятайте: кристали можна об'єднувати в будь-якому порядку!"
        elif context == "army_formation" and problem_type == "multiplication":
            mistake_analysis = "Спробуйте уявити воїнів у рядах та стовпцях - це допоможе з множенням."
        elif context == "depleted_mana" and problem_type == "subtraction":
            mistake_analysis = "Віднімання не комутативне - порядок має значення!"
        else:
            mistake_analysis = "Перечитайте задачу уважно та спробуйте ще раз."
            
        encouragement = "Не здавайтесь! Кожна помилка - це крок до розуміння."

    # Оновлюємо базу даних
    db.commit()
    db.refresh(player_stats)

    return battle_schema.AnswerResult(
        is_correct=is_correct,
        new_player_stats=player_stats,
        xp_gained=xp_gained,
        damage_dealt=damage_dealt,
        new_problem=new_problem_obj,
        feedback_message=feedback_message,
        concept_reinforcement=concept_reinforcement,
        mistake_analysis=mistake_analysis,
        encouragement=encouragement
    )

# Додаємо новий endpoint для отримання підказки
@router.get("/battle/hint/{enemy_id}")
def get_concept_hint(enemy_id: int, db: Session = Depends(deps.get_db), current_user: models.User = Depends(get_current_user)):
    """Повертає концептуальну підказку для поточної задачі"""
    
    enemy = db.query(models.Enemy).filter(models.Enemy.id == enemy_id).first()
    if not enemy:
        raise HTTPException(status_code=404, detail="Enemy not found")
    
    player_stats = db.query(models.PlayerStats).filter(models.PlayerStats.owner_id == current_user.id).first()
    if not player_stats:
        raise HTTPException(status_code=404, detail="Player stats not found")
    
    # Генеруємо приклад задачі для демонстрації концепції
    sample_problem = math_service.generate_problem(topic=enemy.math_topic, level=1)  # Простий приклад
    
    return {
        "topic": enemy.math_topic,
        "concept_explanation": sample_problem.data.get("context_explanation", ""),
        "example": sample_problem.display_text,
        "hint": sample_problem.data.get("concept_hint", "")
    }

# Додати новий endpoint для геометричних підказок
@router.get("/battle/geometry-hint/{problem_type}")
def get_geometry_hint(
    problem_type: str, 
    shape_type: str = "rectangle",
    db: Session = Depends(deps.get_db), 
    current_user: models.User = Depends(get_current_user)
):
    """Повертає інтерактивну підказку для геометричних задач"""
    
    hints = {
        "area": {
            "rectangle": {
                "formula": "Площа = довжина × ширина",
                "visualization_tip": "Уявіть прямокутник поділеним на квадратні одиниці",
                "common_mistakes": ["Плутати площу з периметром", "Забувати одиниці вимірювання"],
                "interactive_demo": True
            },
            "circle": {
                "formula": "Площа = π × радіус²",
                "visualization_tip": "Уявіть коло вписане в квадрат",
                "common_mistakes": ["Використовувати діаметр замість радіуса", "Забувати возводити в квадрат"],
                "interactive_demo": True
            },
            "triangle": {
                "formula": "Площа = ½ × основа × висота або формула Герона",
                "visualization_tip": "Висота завжди перпендикулярна до основи",
                "common_mistakes": ["Використовувати сторону замість висоти", "Забувати ділити на 2"],
                "interactive_demo": True
            }
        },
        "perimeter": {
            "rectangle": {
                "formula": "Периметр = 2 × (довжина + ширина)",
                "visualization_tip": "Уявіть, що йдете навколо фігури",
                "common_mistakes": ["Забувати помножити на 2", "Плутати з площею"]
            },
            "triangle": {
                "formula": "Периметр = сторона₁ + сторона₂ + сторона₃",
                "visualization_tip": "Просто додайте всі сторони",
                "common_mistakes": ["Використовувати висоту замість сторони"]
            }
        },
        "pythagorean": {
            "triangle": {
                "formula": "a² + b² = c², де c - гіпотенуза",
                "visualization_tip": "Гіпотенуза - найдовша сторона, протилежна прямому куту",
                "common_mistakes": ["Плутати катети з гіпотенузою", "Забувати брати квадратний корінь"],
                "theorem_proof": "Можна довести через площі квадратів на сторонах"
            }
        }
    }
    
    hint_data = hints.get(problem_type, {}).get(shape_type, {
        "formula": "Перевірте правильність типу задачі",
        "visualization_tip": "Основи геометрії завжди допоможуть"
    })
    
    return {
        "problem_type": problem_type,
        "shape_type": shape_type,
        **hint_data,
        "interactive_tools": ["ruler", "protractor", "grid"] if hint_data.get("interactive_demo") else []
    }