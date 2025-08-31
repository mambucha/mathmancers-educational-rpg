"""
Прогресивна система навчання алгебри з використанням сучасних педагогічних методик
"""

import random
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
from app.schemas.battle import Problem
from .error_analysis_engine import MathematicalMisconceptionDetector, PersonalizedRemediation

class LearningStage(Enum):
    GUIDED = "guided"           # Повне керівництво з поясненнями
    COLLABORATIVE = "collaborative"  # Підказки та часткова допомога
    INDEPENDENT = "independent"  # Самостійна робота

class ConceptLevel(Enum):
    BALANCE_UNDERSTANDING = "balance"     # Розуміння рівноваги
    INVERSE_OPERATIONS = "inverse"        # Обернені операції  
    SINGLE_STEP = "single_step"          # Одноетапні рівняння
    MULTI_STEP = "multi_step"            # Багатоетапні рівняння

@dataclass
class StudentMastery:
    balance_understanding: float = 0.0    # 0-1
    inverse_operations: float = 0.0       # 0-1  
    equation_solving: float = 0.0         # 0-1
    error_patterns: Dict[str, int] = None # Лічильник помилок по типах
    consecutive_correct: int = 0          # Поспіль правильні
    total_attempts: int = 0               # Загальна кількість спроб
    
    def __post_init__(self):
        if self.error_patterns is None:
            self.error_patterns = {}

class BalanceScaleProblem:
    """Навчання концепції рівноваги через візуальні ваги"""
    
    def __init__(self, a: int, b: int, c: int, stage: LearningStage):
        self.a = a
        self.b = b 
        self.c = c
        self.stage = stage
        self.current_step = 0
        self.steps = self._generate_balance_steps()

    def _generate_balance_steps(self) -> List[Dict]:
        steps = []
        
        # Крок 1: Концептуальне введення
        steps.append({
            "step_type": "concept_intro",
            "title": "Магічні Ваги Рівноваги",
            "equation_display": {
                "left": f"{self.a}x + {self.b}" if self.b != 0 else f"{self.a}x",
                "right": f"{self.c}",
                "balance_state": "balanced"
            },
            "narration": f"Перед вами древні магічні ваги. Ліва чаша важить {self.a}x + {self.b}, права чаша важить {self.c}. Ваги знаходяться у рівновазі.",
            "concept_explanation": "Рівняння - це як ваги. Якщо ми щось додаємо або забираємо, то робимо це з ОБОХ чаш, щоб зберегти рівновагу.",
            "visual_hint": "Зверніть увагу: ваги рівноважні тому, що обидві частини мають однакову 'вагу'."
        })
        
        # Крок 2: Планування дії
        if self.b != 0:
            steps.append({
                "step_type": "planning", 
                "title": "Стратегія Спрощення",
                "current_equation": {
                    "left": f"{self.a}x + {self.b}",
                    "right": f"{self.c}"
                },
                "goal": f"Нашою метою є отримати просто 'x' на лівій чаші. Зараз там {self.a}x + {self.b}.",
                "question": f"Що заважає нам мати просто '{self.a}x' на лівій чаші?",
                "correct_insight": f"Число {self.b} заважає. Його потрібно 'прибрати'.",
                "planning_hint": f"Щоб прибрати {self.b}, потрібно зробити обернену операцію: {'-' if self.b > 0 else '+'}{abs(self.b)}",
                "stage_guidance": self._get_stage_guidance("planning")
            })
        
        # Крок 3: Виконання першої дії  
        if self.b != 0:
            operation = f"- {self.b}" if self.b > 0 else f"+ {abs(self.b)}"
            result_right = self.c - self.b
            
            steps.append({
                "step_type": "execute_operation",
                "title": "Зберігаємо Рівновагу", 
                "question": f"Що робимо з обома частинами рівняння {self.a}x + {self.b} = {self.c}?",
                "correct_operation": operation,
                "options": self._generate_operation_options(self.b, "first_step"),
                "visual_transformation": {
                    "before": {"left": f"{self.a}x + {self.b}", "right": f"{self.c}"},
                    "operation": operation,
                    "after": {"left": f"{self.a}x", "right": f"{result_right}"}
                },
                "explanation": f"Віднімаємо {self.b} з обох частин. Ліва частина: {self.a}x + {self.b} {operation} = {self.a}x. Права частина: {self.c} {operation} = {result_right}.",
                "stage_guidance": self._get_stage_guidance("execute")
            })
        
        # Крок 4: Фінальна дія (якщо a != 1)
        if self.a != 1:
            final_result = (self.c - self.b) // self.a if self.b != 0 else self.c // self.a
            current_right = self.c - self.b if self.b != 0 else self.c
            
            steps.append({
                "step_type": "final_isolation", 
                "title": "Фінальне Виділення x",
                "current_state": {"left": f"{self.a}x", "right": f"{current_right}"},
                "question": f"Як отримати просто 'x' з '{self.a}x'?",
                "correct_operation": f"/ {self.a}",
                "options": self._generate_operation_options(self.a, "final_step"),
                "visual_transformation": {
                    "before": {"left": f"{self.a}x", "right": f"{current_right}"},
                    "operation": f"÷ {self.a}",
                    "after": {"left": "x", "right": f"{final_result}"}
                },
                "explanation": f"Ділимо обидві частини на {self.a}. Отримуємо: x = {final_result}.",
                "celebration": f"Вітаємо! Ви знайшли x = {final_result}. Ваги знову у рівновазі!",
                "stage_guidance": self._get_stage_guidance("final")
            })
        
        return steps

    def _generate_operation_options(self, number: int, step_type: str) -> List[Dict]:
        """Генерує варіанти відповідей з типовими помилками"""
        options = []
        
        if step_type == "first_step":
            # Правильна відповідь
            correct_op = f"- {number}" if number > 0 else f"+ {abs(number)}"
            options.append({
                "operation": correct_op,
                "description": f"Відняти {number} від обох частин" if number > 0 else f"Додати {abs(number)} до обох частин",
                "correct": True,
                "explanation": "Правильно! Це скасує доданок і спростить ліву частину."
            })
            
            # Типові помилки
            wrong_op = f"+ {number}" if number > 0 else f"- {abs(number)}"
            options.append({
                "operation": wrong_op,
                "description": f"Додати {number} до обох частин" if number > 0 else f"Відняти {abs(number)} від обох частин",
                "correct": False,
                "explanation": f"Це ускладнить рівняння замість спрощення. Щоб ПРИБРАТИ {number}, потрібна ОБЕРНЕНА операція.",
                "error_type": "opposite_operation"
            })
            
        elif step_type == "final_step":
            # Правильна відповідь
            options.append({
                "operation": f"/ {number}",
                "description": f"Поділити обидві частини на {number}",
                "correct": True,
                "explanation": f"Правильно! Ділення на {number} скасує множення на {number}."
            })
            
            # Типові помилки
            options.append({
                "operation": f"* {number}",
                "description": f"Помножити обидві частини на {number}",  
                "correct": False,
                "explanation": f"Це ускладнить рівняння. Щоб скасувати множення на {number}, потрібно ПОДІЛИТИ на {number}.",
                "error_type": "wrong_inverse"
            })
        
        # Додаємо випадкові неправильні варіанти
        distractors = [2, 3, 5, 7, 10]
        for d in random.sample([x for x in distractors if x != number], 2):
            options.append({
                "operation": f"- {d}" if step_type == "first_step" else f"/ {d}",
                "description": f"{'Відняти' if step_type == 'first_step' else 'Поділити на'} {d}",
                "correct": False,
                "explanation": f"Неправильне число. Працюйте з числом, яке дійсно присутнє в рівнянні.",
                "error_type": "wrong_number"
            })
        
        random.shuffle(options)
        return options

    def _get_stage_guidance(self, step_type: str) -> Dict[str, str]:
        """Повертає керівництво залежно від рівня навчання студента"""
        guidance = {
            LearningStage.GUIDED: {
                "planning": "Стратегія: Спочатку прибираємо все, що заважає змінній x. Потім виділяємо саму x.",
                "execute": "Підказка: Щоб прибрати число, робимо з ним ОБЕРНЕНУ операцію з ОБОХ боків.",
                "final": "Останній крок: Коефіцієнт при x скасовуємо діленням на цей коефіцієнт."
            },
            LearningStage.COLLABORATIVE: {
                "planning": "Подумайте: що заважає x бути самостійним?",
                "execute": "Яка операція скасує ту, що вже є в рівнянні?", 
                "final": "Як перетворити 'число×x' на просто 'x'?"
            },
            LearningStage.INDEPENDENT: {
                "planning": "",
                "execute": "",
                "final": ""
            }
        }
        
        return {
            "guidance": guidance[self.stage].get(step_type, ""),
            "stage": self.stage.value
        }

class AdaptiveAlgebraEngine:
    """Основний движок адаптивного навчання алгебри з поглибленим аналізом помилок"""
    
    def __init__(self):
        self.student_data = {}  # player_id -> StudentMastery
        self.error_detector = MathematicalMisconceptionDetector()
        self.remediation_engine = PersonalizedRemediation()
        
    def assess_student_level(self, player_id: int, mastery_data: Dict) -> Tuple[LearningStage, ConceptLevel]:
        """Визначає поточний рівень студента"""
        
        student = self.student_data.get(player_id, StudentMastery())
        
        # Визначаємо рівень концепції
        if student.balance_understanding < 0.6:
            concept_level = ConceptLevel.BALANCE_UNDERSTANDING
        elif student.inverse_operations < 0.6:
            concept_level = ConceptLevel.INVERSE_OPERATIONS
        elif student.equation_solving < 0.7:
            concept_level = ConceptLevel.SINGLE_STEP
        else:
            concept_level = ConceptLevel.MULTI_STEP
            
        # Визначаємо рівень підтримки
        overall_mastery = (student.balance_understanding + student.inverse_operations + student.equation_solving) / 3
        
        if overall_mastery < 0.4:
            learning_stage = LearningStage.GUIDED
        elif overall_mastery < 0.7:
            learning_stage = LearningStage.COLLABORATIVE
        else:
            learning_stage = LearningStage.INDEPENDENT
            
        return learning_stage, concept_level

    def generate_adaptive_algebra_problem(self, player_id: int, level: int) -> Problem:
        """Генерує алгебраїчну задачу, адаптовану до рівня студента"""
        
        # Отримуємо або створюємо дані студента
        student = self.student_data.get(player_id, StudentMastery())
        self.student_data[player_id] = student
        
        learning_stage, concept_level = self.assess_student_level(player_id, student.__dict__)
        
        # Генеруємо рівняння відповідної складності
        if concept_level in [ConceptLevel.BALANCE_UNDERSTANDING, ConceptLevel.SINGLE_STEP]:
            a = random.choice([2, 3, 4, 5])
            b = random.randint(1, 10) * random.choice([-1, 1])
            x_value = random.randint(2, 8)
            c = a * x_value + b
        else:
            # Складніші рівняння для просунутих студентів
            a = random.choice([2, 3, 4, 5, 6])  
            b = random.randint(5, 15) * random.choice([-1, 1])
            x_value = random.randint(3, 12)
            c = a * x_value + b
            
        # Створюємо прогресивну задачу
        balance_problem = BalanceScaleProblem(a, b, c, learning_stage)
        
        return Problem(
            display_text=self._create_contextual_intro(learning_stage, concept_level),
            data={
                "type": "progressive_equation",
                "equation_parts": {"a": a, "b": b, "c": c, "x_isolated": False},
                "balance_steps": balance_problem.steps,
                "current_step": 0,
                "learning_stage": learning_stage.value,
                "concept_level": concept_level.value,
                "player_mastery": student.__dict__,
                "adaptive_features": {
                    "show_visual_aids": learning_stage != LearningStage.INDEPENDENT,
                    "provide_hints": learning_stage == LearningStage.GUIDED,
                    "error_analysis": True
                }
            },
            answer=x_value
        )

    def _create_contextual_intro(self, stage: LearningStage, level: ConceptLevel) -> str:
        """Створює контекстуальне введення залежно від рівня"""
        
        intros = {
            ConceptLevel.BALANCE_UNDERSTANDING: [
                "Древні арифмансери використовували магічні ваги для розв'язування рівнянь. Навчіться їхньому мистецтву!",
                "Перед вами таємна техніка рівноваги. Магічні ваги допоможуть знайти невідоме число.",
                "Легендарні математичні ваги чекають на вас. Дізнайтеся, як зберегти рівновагу при пошуку x."
            ],
            ConceptLevel.SINGLE_STEP: [
                "Застосуйте техніку магічних ваг для розв'язання цього рівняння.",
                "Використайте принцип рівноваги для знаходження невідомої."
            ],
            ConceptLevel.MULTI_STEP: [
                "Складне рівняння потребує майстерності арифмансера. Покажіть свою майстерність!",
                "Багатоетапна магія рівноваги. Готові до виклику?"
            ]
        }
        
        return random.choice(intros.get(level, intros[ConceptLevel.BALANCE_UNDERSTANDING]))

    def process_student_response(self, player_id: int, problem_data: Dict, 
                                chosen_operation: str) -> Dict[str, Any]:
        """Обробляє відповідь студента з детальним аналізом"""
        
        student = self.student_data.get(player_id, StudentMastery())
        steps = problem_data.get("balance_steps", [])
        current_step_idx = problem_data.get("current_step", 0)
        
        if current_step_idx >= len(steps):
            return {"error": "Invalid step index"}
            
        current_step = steps[current_step_idx]
        student.total_attempts += 1
        
        # Знаходимо правильну відповідь
        correct_option = None
        chosen_option = None
        
        for option in current_step.get("options", []):
            if option["correct"]:
                correct_option = option
            if option["operation"] == chosen_operation:
                chosen_option = option
                
        is_correct = chosen_option and chosen_option["correct"]
        
        if is_correct:
            student.consecutive_correct += 1
            self._update_mastery_on_success(student, current_step["step_type"])
            
            # Переходимо до наступного кроку
            next_step_idx = current_step_idx + 1
            is_completed = next_step_idx >= len(steps)
            
            response = {
                "is_correct": True,
                "feedback": chosen_option["explanation"],
                "next_step": next_step_idx if not is_completed else None,
                "is_equation_solved": is_completed,
                "mastery_update": self._get_mastery_feedback(student),
                "visual_transformation": current_step.get("visual_transformation"),
                "celebration": current_step.get("celebration", "")
            }
            
        else:
            student.consecutive_correct = 0
            error_analysis = self._analyze_error(
                chosen_option, correct_option, student, 
                {"equation_parts": steps[0].get("equation_parts", {}), "current_step": current_step_idx}
            )
            self._update_mastery_on_error(student, error_analysis)
            
            # Використовуємо персоналізовану допомогу
            personalized_help = error_analysis.get("personalized_help", {})
            
            response = {
                "is_correct": False,
                "feedback": chosen_option["explanation"] if chosen_option else "Неправильний вибір",
                "error_analysis": error_analysis,
                "remediation": personalized_help.get("explanation", "Спробуйте ще раз"),
                "detailed_help": {
                    "primary_issue": personalized_help.get("primary_issue", "unknown"),
                    "analogy": personalized_help.get("analogy", ""),
                    "practice_tip": personalized_help.get("practice_tip", ""),
                    "visual_aid": personalized_help.get("visual_aid", ""),
                    "confidence": error_analysis.get("confidence", 0.5),
                    "severity": error_analysis.get("severity", 0.5)
                },
                "encouragement": personalized_help.get("encouragement", self._get_encouragement(student)),
                "next_step": current_step_idx  # Повторюємо той самий крок
            }
            
        self.student_data[player_id] = student
        return response

    def _update_mastery_on_success(self, student: StudentMastery, step_type: str):
        """Оновлює майстерність при правильній відповіді"""
        improvement = 0.1 + (0.05 if student.consecutive_correct > 3 else 0)
        
        if step_type in ["concept_intro", "planning"]:
            student.balance_understanding = min(1.0, student.balance_understanding + improvement)
        elif step_type in ["execute_operation", "final_isolation"]:
            student.inverse_operations = min(1.0, student.inverse_operations + improvement)
            student.equation_solving = min(1.0, student.equation_solving + improvement * 0.8)

    def _analyze_error(self, chosen_option: Dict, correct_option: Dict, 
                      student: StudentMastery, equation_context: Dict) -> Dict[str, Any]:
        """Поглиблений аналіз помилки студента"""
        if not chosen_option:
            return {
                "error_type": "no_selection",
                "pattern": "Не обрано жодного варіанту",
                "frequency": 1,
                "detailed_analysis": None,
                "personalized_help": {"message": "Оберіть одну з запропонованих операцій"}
            }
            
        # Використовуємо новий детектор заблуждень
        error_patterns = self.error_detector.analyze_student_error(
            correct_option.get("operation", ""),
            chosen_option.get("operation", ""),
            equation_context,
            student.__dict__
        )
        
        # Генеруємо персоналізовану допомогу
        student_profile = {
            'learning_style': self._infer_learning_style(student),
            'mastery_level': (student.balance_understanding + student.inverse_operations) / 2
        }
        
        personalized_help = self.remediation_engine.generate_personalized_help(
            error_patterns, 
            student_profile
        )
        
        # Оновлюємо частоту помилок
        primary_error = error_patterns[0] if error_patterns else None
        if primary_error:
            error_type = primary_error.misconception_type.value
            student.error_patterns[error_type] = student.error_patterns.get(error_type, 0) + 1
        else:
            error_type = "unknown_error"
            student.error_patterns[error_type] = student.error_patterns.get(error_type, 0) + 1
        
        return {
            "error_type": error_type,
            "pattern": chosen_option.get("explanation", ""),
            "frequency": student.error_patterns[error_type],
            "is_recurring": student.error_patterns[error_type] > 2,
            "detailed_analysis": error_patterns[0] if error_patterns else None,
            "personalized_help": personalized_help,
            "confidence": primary_error.confidence if primary_error else 0.5,
            "severity": primary_error.severity if primary_error else 0.5
        }

    def _infer_learning_style(self, student: StudentMastery) -> str:
        """Визначає стиль навчання на основі поведінки студента"""
        
        # Аналізуємо паттерни помилок для визначення стилю
        error_patterns = student.error_patterns
        
        visual_indicators = error_patterns.get('balance_violation', 0) + error_patterns.get('equation_statement', 0)
        procedural_indicators = error_patterns.get('operation_reversal', 0) + error_patterns.get('procedural_error', 0)
        
        if visual_indicators > procedural_indicators:
            return 'visual'
        elif procedural_indicators > visual_indicators:
            return 'procedural'
        else:
            return 'balanced'

    def _get_mastery_feedback(self, student: StudentMastery) -> Dict[str, Any]:
        """Повертає інформацію про прогрес"""
        return {
            "balance_mastery": student.balance_understanding,
            "operations_mastery": student.inverse_operations, 
            "equation_mastery": student.equation_solving,
            "streak": student.consecutive_correct,
            "ready_for_next_level": (
                student.balance_understanding > 0.7 and 
                student.inverse_operations > 0.7 and
                student.consecutive_correct >= 3
            )
        }

    def _update_mastery_on_error(self, student: StudentMastery, error_analysis: Dict):
        """Оновлює майстерність при помилці"""
        # Незначне зменшення майстерності при помилках
        penalty = 0.02
        student.balance_understanding = max(0.0, student.balance_understanding - penalty)
        student.inverse_operations = max(0.0, student.inverse_operations - penalty)
        student.equation_solving = max(0.0, student.equation_solving - penalty)

    def _get_encouragement(self, student: StudentMastery) -> str:
        """Генерує підбадьорливі повідомлення"""
        if student.total_attempts <= 3:
            return "Не хвилюйтеся, навчання потребує часу. Продовжуйте спробувати!"
        elif student.consecutive_correct == 0 and student.total_attempts > 5:
            return "Математика може бути складною, але ви на правильному шляху. Кожна помилка - це урок!"
        else:
            return "Чудово працюєте! Продовжуйте в тому ж дусі."