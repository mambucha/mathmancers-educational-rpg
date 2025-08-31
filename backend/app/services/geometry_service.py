"""
Інтелектуальна система геометричних задач для MathMancers
Створює інтерактивні геометричні виклики з візуалізацією
"""

import random
import math
from typing import Dict, List, Any, Tuple
from app.schemas.battle import Problem

class GeometricShape:
    """Базовий клас для геометричних фігур"""
    
    def __init__(self, name: str, properties: Dict[str, float]):
        self.name = name
        self.properties = properties
        
    def get_area(self) -> float:
        raise NotImplementedError
    
    def get_perimeter(self) -> float:
        raise NotImplementedError
    
    def get_visualization_data(self) -> Dict[str, Any]:
        raise NotImplementedError

class Rectangle(GeometricShape):
    def __init__(self, width: float, height: float):
        super().__init__("rectangle", {"width": width, "height": height})
        self.width = width
        self.height = height
    
    def get_area(self) -> float:
        return self.width * self.height
    
    def get_perimeter(self) -> float:
        return 2 * (self.width + self.height)
    
    def get_visualization_data(self) -> Dict[str, Any]:
        return {
            "type": "rectangle",
            "width": self.width,
            "height": self.height,
            "vertices": [
                {"x": 0, "y": 0},
                {"x": self.width, "y": 0},
                {"x": self.width, "y": self.height},
                {"x": 0, "y": self.height}
            ]
        }

class Circle(GeometricShape):
    def __init__(self, radius: float):
        super().__init__("circle", {"radius": radius})
        self.radius = radius
    
    def get_area(self) -> float:
        return math.pi * self.radius ** 2
    
    def get_perimeter(self) -> float:
        return 2 * math.pi * self.radius
    
    def get_visualization_data(self) -> Dict[str, Any]:
        return {
            "type": "circle",
            "radius": self.radius,
            "center": {"x": self.radius, "y": self.radius}
        }

class Triangle(GeometricShape):
    def __init__(self, a: float, b: float, c: float):
        super().__init__("triangle", {"a": a, "b": b, "c": c})
        self.a, self.b, self.c = a, b, c
        
        # Перевіряємо валідність трикутника
        if not (a + b > c and b + c > a and a + c > b):
            raise ValueError("Invalid triangle sides")
    
    def get_area(self) -> float:
        # Формула Герона
        s = (self.a + self.b + self.c) / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))
    
    def get_perimeter(self) -> float:
        return self.a + self.b + self.c
    
    def get_visualization_data(self) -> Dict[str, Any]:
        # Розміщуємо трикутник на координатній площині
        # A в (0,0), B в (c,0), C обчислюємо за законом косинусів
        cos_A = (self.b**2 + self.c**2 - self.a**2) / (2 * self.b * self.c)
        C_x = self.b * cos_A
        C_y = self.b * math.sqrt(1 - cos_A**2) if cos_A**2 <= 1 else 0
        
        return {
            "type": "triangle",
            "sides": {"a": self.a, "b": self.b, "c": self.c},
            "vertices": [
                {"x": 0, "y": 0},
                {"x": self.c, "y": 0},
                {"x": C_x, "y": C_y}
            ]
        }

class GeometryPuzzleGenerator:
    """Генератор інтелектуальних геометричних головоломок"""
    
    STORY_CONTEXTS = {
        "fortress_blueprints": {
            "setup": "Архітектор плануєчарівну фортецю. Допоможіть розрахувати її параметри:",
            "success": "Фортеця побудована міцно! Вороги не пройдуть.",
            "failure": "Стіни обвалились через неправильні розрахунки!"
        },
        "magic_portals": {
            "setup": "Древні портали мають особливу геометрію. Розгадайте їх секрет:",
            "success": "Портал активовано! Магічна енергія тече вільно.",
            "failure": "Портал нестабільний через помилкові вимірювання!"
        },
        "crystal_formations": {
            "setup": "Магічні кристали ростуть у геометричних формах. Обчисліть їх силу:",
            "success": "Кристал резонує з правильною частотою!",
            "failure": "Кристал тріскається від неточних обчислень!"
        }
    }
    
    def __init__(self):
        self.difficulty_ranges = {
            1: {"min": 3, "max": 8},      # Легкий
            2: {"min": 5, "max": 12},     # Середній  
            3: {"min": 8, "max": 20},     # Складний
            4: {"min": 12, "max": 30},    # Експертний
        }
    
    def generate_geometry_challenge(self, level: int = 1, challenge_type: str = "area") -> Problem:
        """Генерує геометричну головоломку залежно від рівня"""
        
        difficulty = min(max(level, 1), 4)
        range_vals = self.difficulty_ranges[difficulty]
        context = random.choice(list(self.STORY_CONTEXTS.keys()))
        
        if challenge_type == "area":
            return self._generate_area_challenge(range_vals, context, level)
        elif challenge_type == "perimeter":
            return self._generate_perimeter_challenge(range_vals, context, level)
        elif challenge_type == "pythagorean":
            return self._generate_pythagorean_challenge(range_vals, context, level)
        else:
            return self._generate_area_challenge(range_vals, context, level)
    
    def _generate_area_challenge(self, range_vals: Dict, context: str, level: int) -> Problem:
        """Генерує задачу на обчислення площі"""
        
        shape_choice = random.choice(["rectangle", "circle", "triangle"])
        story_data = self.STORY_CONTEXTS[context]
        
        if shape_choice == "rectangle":
            width = random.randint(range_vals["min"], range_vals["max"])
            height = random.randint(range_vals["min"], range_vals["max"])
            shape = Rectangle(width, height)
            
            problem_text = f"{story_data['setup']} Прямокутна {self._get_context_object(context)} має розміри {width} на {height} метрів. Яка її площа?"
            
        elif shape_choice == "circle":
            radius = random.randint(range_vals["min"], range_vals["max"] // 2)
            shape = Circle(radius)
            
            problem_text = f"{story_data['setup']} Кругла {self._get_context_object(context)} має радіус {radius} метрів. Яка її площа? (Використайте π ≈ 3.14)"
            
        else:  # triangle
            # Генеруємо валідний трикутник
            a = random.randint(range_vals["min"], range_vals["max"])
            b = random.randint(range_vals["min"], range_vals["max"]) 
            c = random.randint(max(1, abs(a-b)+1), a+b-1)  # Забезпечуємо нерівність трикутника
            
            shape = Triangle(a, b, c)
            problem_text = f"{story_data['setup']} Трикутна {self._get_context_object(context)} має сторони {a}, {b} та {c} метрів. Яка її площа? (Округліть до цілого)"
        
        return Problem(
            display_text=problem_text,
            data={
                "type": "geometry",
                "challenge_type": "area", 
                "shape": shape.get_visualization_data(),
                "context": context,
                "level": level,
                "story_feedback": story_data,
                "hint": self._generate_hint("area", shape_choice),
                "step_by_step": self._generate_solution_steps("area", shape),
                "interactive_features": {
                    "manipulatable": True,
                    "show_grid": True,
                    "highlight_measurements": True
                }
            },
            answer=int(round(shape.get_area()))
        )
    
    def _generate_perimeter_challenge(self, range_vals: Dict, context: str, level: int) -> Problem:
        """Генерує задачу на обчислення периметру"""
        
        shape_choice = random.choice(["rectangle", "triangle"])
        story_data = self.STORY_CONTEXTS[context]
        
        if shape_choice == "rectangle":
            width = random.randint(range_vals["min"], range_vals["max"])
            height = random.randint(range_vals["min"], range_vals["max"])
            shape = Rectangle(width, height)
            
            problem_text = f"{story_data['setup']} Потрібно огородити {self._get_context_object(context)} розміром {width} на {height} метрів. Скільки метрів огорожі потрібно?"
            
        else:  # triangle
            a = random.randint(range_vals["min"], range_vals["max"])
            b = random.randint(range_vals["min"], range_vals["max"])
            c = random.randint(max(1, abs(a-b)+1), a+b-1)
            
            shape = Triangle(a, b, c)
            problem_text = f"{story_data['setup']} Трикутний {self._get_context_object(context)} має сторони {a}, {b} та {c} метрів. Який його периметр?"
        
        return Problem(
            display_text=problem_text,
            data={
                "type": "geometry",
                "challenge_type": "perimeter",
                "shape": shape.get_visualization_data(),
                "context": context,
                "level": level,
                "story_feedback": story_data,
                "hint": self._generate_hint("perimeter", shape_choice),
                "step_by_step": self._generate_solution_steps("perimeter", shape)
            },
            answer=int(round(shape.get_perimeter()))
        )
    
    def _generate_pythagorean_challenge(self, range_vals: Dict, context: str, level: int) -> Problem:
        """Генерує задачу на теорему Піфагора"""
        
        story_data = self.STORY_CONTEXTS[context]
        
        # Генеруємо прямокутний трикутник
        a = random.randint(3, range_vals["max"] // 2)
        b = random.randint(4, range_vals["max"] // 2) 
        c = math.sqrt(a**2 + b**2)
        
        # Випадково обираємо, що шукати
        unknown = random.choice(['a', 'b', 'c'])
        
        if unknown == 'c':
            problem_text = f"{story_data['setup']} Прямокутний трикутник має катети {a} та {b} метрів. Знайдіть гіпотенузу. (Округліть до цілого)"
            answer = int(round(c))
            given_values = {"a": a, "b": b}
        elif unknown == 'a':
            problem_text = f"{story_data['setup']} Прямокутний трикутник має катет {b} метрів та гіпотенузу {int(round(c))} метрів. Знайдіть другий катет. (Округліть до цілого)"
            answer = a
            given_values = {"b": b, "c": int(round(c))}
        else:  # unknown == 'b'
            problem_text = f"{story_data['setup']} Прямокутний трикутник має катет {a} метрів та гіпотенузу {int(round(c))} метрів. Знайдіть другий катет. (Округліть до цілого)"
            answer = b
            given_values = {"a": a, "c": int(round(c))}
        
        return Problem(
            display_text=problem_text,
            data={
                "type": "geometry", 
                "challenge_type": "pythagorean",
                "unknown_side": unknown,
                "given_values": given_values,
                "context": context,
                "level": level,
                "story_feedback": story_data,
                "hint": "Пам'ятайте: a² + b² = c², де c - гіпотенуза",
                "theorem_visualization": {
                    "show_squares": True,
                    "animate_proof": True
                }
            },
            answer=answer
        )
    
    def _get_context_object(self, context: str) -> str:
        """Повертає об'єкт відповідно до контексту"""
        objects = {
            "fortress_blueprints": random.choice(["фортеця", "вежа", "стіна", "подвір'я"]),
            "magic_portals": random.choice(["портал", "брама", "коло телепортації", "магічна зона"]),
            "crystal_formations": random.choice(["кристал", "формація", "магічний камінь", "енергетичне поле"])
        }
        return objects.get(context, "область")
    
    def _generate_hint(self, challenge_type: str, shape: str) -> str:
        """Генерує підказку для задачі"""
        hints = {
            ("area", "rectangle"): "Площа прямокутника = довжина × ширина",
            ("area", "circle"): "Площа кола = π × радіус²",
            ("area", "triangle"): "Використайте формулу Герона або ½ × основа × висота",
            ("perimeter", "rectangle"): "Периметр = 2 × (довжина + ширина)",
            ("perimeter", "triangle"): "Периметр = сума всіх сторін",
        }
        return hints.get((challenge_type, shape), "Подумайте про властивості фігури")
    
    def _generate_solution_steps(self, challenge_type: str, shape: GeometricShape) -> List[str]:
        """Генерує покрокове рішення"""
        if challenge_type == "area":
            if isinstance(shape, Rectangle):
                return [
                    f"1. Визначаємо формулу площі: S = довжина × ширина",
                    f"2. Підставляємо значення: S = {shape.width} × {shape.height}",
                    f"3. Обчислюємо: S = {shape.get_area()}"
                ]
            elif isinstance(shape, Circle):
                return [
                    f"1. Формула площі кола: S = π × r²",
                    f"2. Підставляємо: S = 3.14 × {shape.radius}²",
                    f"3. Обчислюємо: S = 3.14 × {shape.radius**2} = {round(shape.get_area(), 2)}"
                ]
        return ["Крок за кроком розв'яжіть задачу"]

# Глобальний екземпляр генератора
geometry_generator = GeometryPuzzleGenerator()

def generate_geometry_problem(level: int = 1, challenge_type: str = "area") -> Problem:
    """Головна функція для генерації геометричних задач"""
    return geometry_generator.generate_geometry_challenge(level, challenge_type)

def generate_geometric_titan_encounter(player_level: int) -> Tuple[Problem, Dict[str, Any]]:
    """Генерує зустріч з Геометричним Титаном"""
    
    # Титан адаптується до рівня гравця
    challenge_types = ["area", "perimeter"]
    if player_level >= 3:
        challenge_types.append("pythagorean")
    
    challenge_type = random.choice(challenge_types)
    problem = generate_geometry_problem(player_level, challenge_type)
    
    # Особливості Геометричного Титана
    titan_data = {
        "name": "Геометричний Титан",
        "description": "Велетенський страж, складений з рухомих геометричних фігур",
        "current_form": problem.data["shape"]["type"], 
        "transformation_ability": True,
        "weakness": "точні геометричні розрахунки",
        "battle_phrases": [
            "Мої форми ідеальні! Твої обчислення - ні!",
            "Кожен мій кут розрахований для перемоги!",
            "Геометрія - це порядок. Ти ж приносиш хаос!"
        ]
    }
    
    return problem, titan_data