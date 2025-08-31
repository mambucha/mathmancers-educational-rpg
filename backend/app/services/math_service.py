import random
from app.schemas.battle import Problem
from typing import Dict, Any, List
from .progressive_algebra_engine import AdaptiveAlgebraEngine
from .geometry_service import generate_geometry_problem, generate_geometric_titan_encounter

class ConceptContext:
    """Контекст для математичних концепцій у світі MathMancers"""
    
    STORY_CONTEXTS = {
        "addition": [
            "magic_crystals", "army_units", "spell_ingredients", 
            "treasure_coins", "potion_bottles"
        ],
        "subtraction": [
            "depleted_mana", "fallen_warriors", "consumed_potions",
            "spent_coins", "broken_crystals"
        ],
        "multiplication": [
            "army_formation", "crystal_grids", "spell_patterns",
            "tower_floors", "magic_circles"
        ],
        "geometry": [
            "fortress_blueprints", "magic_portals", "enchanted_gardens",
            "crystal_formations", "spell_diagrams"
        ],
        "algebra": [
            "ancient_scrolls", "magical_equations", "balance_stones",
            "cipher_runes", "arithmetic_mysteries"
        ]
    }
    
    @staticmethod
    def get_story_template(operation: str, context: str) -> Dict[str, str]:
        """Повертає шаблони історій для різних операцій та контекстів"""
        templates = {
            "addition": {
                "magic_crystals": {
                    "setup": "У вашій лабораторії є {num1} світлих кристалів. Ви знайшли ще {num2} темних кристалів.",
                    "question": "Скільки всього кристалів у вас тепер?",
                    "concept_hint": "Магічна властивість: світлі + темні = темні + світлі. Чому порядок не важливий?",
                    "context_explanation": "Кристали можна об'єднувати у будь-якому порядку - це комутативна властивість додавання."
                },
                "army_units": {
                    "setup": "Ваша армія складається з {num1} лучників та {num2} мечників.",
                    "question": "Скільки всього воїнів у вашій армії?",
                    "concept_hint": "Військова стратегія: {num1} + {num2} = {num2} + {num1}",
                    "context_explanation": "Незалежно від того, як ви рахуєте війська, їх загальна кількість не зміниться."
                }
            },
            "multiplication": {
                "army_formation": {
                    "setup": "Ви розставляєте армію у {num1} рядів по {num2} воїнів у кожному.",
                    "question": "Скільки всього воїнів у формації?",
                    "concept_hint": "Магічна симетрія: {num1}×{num2} = {num2}×{num1}",
                    "context_explanation": "Можна розставити {num1} рядів по {num2} або {num2} рядів по {num1} - результат однаковий!"
                },
                "crystal_grids": {
                    "setup": "Ви створюєте магічну сітку з {num1} стовпців, кожен містить {num2} кристалів.",
                    "question": "Скільки кристалів потрібно для повної сітки?",
                    "concept_hint": "Енергія сітки: {num1} × {num2} = сила × кількість",
                    "context_explanation": "Сітка із {num1}×{num2} має таку ж потужність, як {num2}×{num1}."
                }
            },
            "subtraction": {
                "depleted_mana": {
                    "setup": "У вас було {num1} одиниць мани. Ви витратили {num2} на потужне заклинання.",
                    "question": "Скільки мани залишилось?",
                    "concept_hint": "Обережно! {num1} - {num2} ≠ {num2} - {num1}",
                    "context_explanation": "На відміну від додавання, віднімання не є комутативним - порядок має значення!"
                }
            }
        }
        
        return templates.get(operation, {}).get(context, {
            "setup": "Виконайте обчислення:",
            "question": "{num1} {operation} {num2} = ?",
            "concept_hint": "Знайдіть правильну відповідь",
            "context_explanation": "Базова математична операція"
        })

class StoryBasedProblem:
    """Клас для створення задач з ігровим контекстом та концептуальними поясненнями"""
    
    def __init__(self, operation: str, num1: int, num2: int, answer: int, context: str = None):
        self.operation = operation
        self.num1 = num1
        self.num2 = num2
        self.answer = answer
        self.context = context or random.choice(ConceptContext.STORY_CONTEXTS.get(operation, ["basic"]))
        self.template = ConceptContext.get_story_template(operation, self.context)
    
    def to_problem(self) -> Problem:
        """Конвертує у Problem для API"""
        
        # Створюємо повний текст задачі
        setup = self.template.get("setup", "").format(num1=self.num1, num2=self.num2)
        question = self.template.get("question", "").format(
            num1=self.num1, 
            num2=self.num2, 
            operation=self.operation
        )
        
        display_text = f"{setup} {question}"
        
        return Problem(
            display_text=display_text,
            data={
                "operation": self.operation,
                "num1": self.num1,
                "num2": self.num2,
                "context": self.context,
                "concept_hint": self.template.get("concept_hint", "").format(
                    num1=self.num1, num2=self.num2, operation=self.operation
                ),
                "context_explanation": self.template.get("context_explanation", ""),
                "difficulty_factors": self._analyze_difficulty()
            },
            answer=self.answer
        )
    
    def _analyze_difficulty(self) -> Dict[str, Any]:
        """Аналізує складність задачі для адаптивної системи"""
        return {
            "number_size": max(self.num1, self.num2),
            "operation_complexity": {
                "addition": 1,
                "subtraction": 2,
                "multiplication": 3,
                "division": 4
            }.get(self.operation, 1),
            "context_complexity": {
                "basic": 1,
                "magic_crystals": 2,
                "army_formation": 3,
                "fortress_blueprints": 4
            }.get(self.context, 1)
        }

def generate_problem(topic: str, level: int = 1, player_id: int = None) -> Problem:
    """Оновлений генератор з підтримкою геометрії"""
    
    if topic == "addition":
        return _generate_conceptual_addition(level)
    elif topic == "subtraction":
        return _generate_conceptual_subtraction(level)
    elif topic == "multiplication":
        return _generate_conceptual_multiplication(level)
    elif topic == "geometry":
        return _generate_enhanced_geometry(level)
    elif topic == "algebra":
        return _generate_algebra_problem(level, player_id)
    else:
        return _generate_conceptual_addition(level)

def _generate_conceptual_addition(level: int) -> Problem:
    """Генерує задачі на додавання з ігровим контекстом"""
    
    # Адаптивна складність
    if level == 1:
        num1 = random.randint(1, 5)
        num2 = random.randint(1, 5)
    elif level <= 3:
        num1 = random.randint(3, 12)
        num2 = random.randint(3, 12)
    else:
        num1 = random.randint(10, 25)
        num2 = random.randint(10, 25)
    
    answer = num1 + num2
    
    story_problem = StoryBasedProblem("addition", num1, num2, answer)
    return story_problem.to_problem()

def _generate_conceptual_subtraction(level: int) -> Problem:
    """Генерує задачі на віднімання з акцентом на некомутативність"""
    
    # Завжди num1 > num2 для уникнення від'ємних результатів
    if level == 1:
        num1 = random.randint(6, 10)
        num2 = random.randint(1, num1 - 1)
    elif level <= 3:
        num1 = random.randint(15, 30)
        num2 = random.randint(5, num1 - 5)
    else:
        num1 = random.randint(25, 50)
        num2 = random.randint(10, num1 - 10)
    
    answer = num1 - num2
    
    story_problem = StoryBasedProblem("subtraction", num1, num2, answer)
    return story_problem.to_problem()

def _generate_conceptual_multiplication(level: int) -> Problem:
    """Генерує задачі на множення з візуальним контекстом формацій"""
    
    if level == 1:
        num1 = random.randint(2, 5)
        num2 = random.randint(2, 5)
    elif level <= 3:
        num1 = random.randint(3, 8)
        num2 = random.randint(2, 7)
    else:
        num1 = random.randint(6, 12)
        num2 = random.randint(4, 9)
    
    answer = num1 * num2
    
    story_problem = StoryBasedProblem("multiplication", num1, num2, answer)
    return story_problem.to_problem()

def _generate_enhanced_geometry(level: int) -> Problem:
    """Генерує складні геометричні задачі з інтерактивними елементами"""
    
    # Визначаємо тип виклику залежно від рівня
    if level <= 2:
        challenge_types = ["area", "perimeter"]
    else:
        challenge_types = ["area", "perimeter", "pythagorean"]
    
    challenge_type = random.choice(challenge_types)
    return generate_geometry_problem(level, challenge_type)

# Створюємо глобальний екземпляр адаптивного движка
adaptive_engine = AdaptiveAlgebraEngine()

def _generate_algebra_problem(level: int, player_id: int = None) -> Problem:
    """Генерує лінійне рівняння з вибором правильних і неправильних операцій."""
    
    # Якщо є player_id, використовуємо прогресивну систему
    if player_id is not None:
        return adaptive_engine.generate_adaptive_algebra_problem(player_id, level)
    
    # Fallback до старої системи
    a = random.randint(2, 5)
    x = random.randint(2, 5 * level)
    b = random.randint(1, 10 * level)
    c = a * x + b

    # Правильна послідовність кроків
    solution_steps = [
        {"operation": f"- {b}", "description": f"Відняти {b} від обох частин", "correct": True},
        {"operation": f"/ {a}", "description": f"Поділити обидві частини на {a}", "correct": True}
    ]

    # Генеруємо неправильні варіанти для кожного кроку
    def generate_wrong_operations(step_index, a_val, b_val):
        wrong_ops = []
        if step_index == 0:  # Перший крок - операція з b
            wrong_ops.extend([
                {"operation": f"+ {b_val}", "description": f"Додати {b_val} до обох частин", "correct": False},
                {"operation": f"* {b_val}", "description": f"Помножити обидві частини на {b_val}", "correct": False},
                {"operation": f"/ {b_val}", "description": f"Поділити обидві частини на {b_val}", "correct": False}
            ])
            
            other_nums = [num for num in range(1, 15) if num != b_val and num != a_val]
            for num in random.sample(other_nums, min(3, len(other_nums))):
                wrong_ops.append({
                    "operation": f"- {num}", 
                    "description": f"Відняти {num} від обох частин", 
                    "correct": False
                })
                
        else:  # Другий крок - операція з a
            wrong_ops.extend([
                {"operation": f"+ {a_val}", "description": f"Додати {a_val} до обох частин", "correct": False},
                {"operation": f"- {a_val}", "description": f"Відняти {a_val} від обох частин", "correct": False},
                {"operation": f"* {a_val}", "description": f"Помножити обидві частини на {a_val}", "correct": False}
            ])
            
            other_nums = [2, 3, 4, 5, 6, 7, 8]
            for num in other_nums:
                if num != a_val:
                    wrong_ops.append({
                        "operation": f"/ {num}", 
                        "description": f"Поділити обидві частини на {num}", 
                        "correct": False
                    })
        
        return random.sample(wrong_ops, min(3, len(wrong_ops)))

    for i, step in enumerate(solution_steps):
        step["wrong_options"] = generate_wrong_operations(i, a, b)

    return Problem(
        display_text=f"Древній арифмансер залишив рівняння-загадку. Розв'яжіть його, обираючи правильні кроки:",
        data={
            "type": "equation",
            "equation_parts": {"a": a, "b": b, "c": c, "x_isolated": False},
            "solution_steps": solution_steps,
            "current_step_index": 0,
            "context": "ancient_puzzle",
            "concept_hint": "Рівняння - це магічні ваги. Що робите з одним боком, робіть і з іншим!",
            "context_explanation": "Арифмансери використовували рівняння для шифрування секретів."
        },
        answer=x
    )

def generate_special_encounter(enemy_name: str, player_level: int) -> tuple:
    """Генерує спеціальні зустрічі з унікальними ворогами"""
    
    if enemy_name == "Geometric Titan" or "geometric" in enemy_name.lower():
        return generate_geometric_titan_encounter(player_level)
    
    # Fallback для інших ворогів
    problem = generate_problem("addition", player_level)
    encounter_data = {
        "name": enemy_name,
        "description": "Таємничий математичний ворог",
        "special_abilities": []
    }
    
    return problem, encounter_data

# Fallback функція для сумісності
def _generate_geometry_problem(level: int = 1) -> Problem:
    width = random.randint(3 * level, 10 * level)
    height = random.randint(3 * level, 10 * level)

    return Problem(
        display_text=f"Знайдіть площу прямокутника зі сторонами {width} та {height}",
        data={"shape": "rectangle", "width": width, "height": height},
        answer=width * height
    )