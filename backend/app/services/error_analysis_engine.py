"""
Система глибокого аналізу математичних помилок та заблуждень
"""

from typing import Dict, List, Any, Tuple, Optional
from enum import Enum
from dataclasses import dataclass
import re

class MisconceptionType(Enum):
    """Типи математичних заблуждень на основі досліджень"""
    EQUATION_AS_STATEMENT = "equation_statement"           # Рівняння як твердження
    OPERATION_REVERSAL = "operation_reversal"              # Плутання обернених операцій
    SIGN_ERROR = "sign_error"                              # Помилки із знаками
    COEFFICIENT_CONFUSION = "coefficient_confusion"        # Плутання коефіцієнтів
    ORDER_OF_OPERATIONS = "order_operations"               # Порядок дій
    VARIABLE_MISCONCEPTION = "variable_misconception"      # Нерозуміння змінних
    BALANCE_VIOLATION = "balance_violation"                # Порушення рівноваги
    PROCEDURAL_ERROR = "procedural_error"                  # Механічні помилки

@dataclass
class ErrorPattern:
    """Паттерн помилки з контекстом"""
    misconception_type: MisconceptionType
    confidence: float  # 0-1, наскільки впевнені в діагнозі
    evidence: List[str]  # Докази цієї помилки
    frequency: int  # Скільки раз зустрічалась у цього учня
    severity: float  # 0-1, критичність для навчання

class MathematicalMisconceptionDetector:
    """Детектор математичних заблуждень"""
    
    def __init__(self):
        self.misconception_patterns = self._initialize_patterns()
        self.remediation_strategies = self._initialize_remediation()
    
    def _initialize_patterns(self) -> Dict[MisconceptionType, Dict]:
        """Ініціалізує паттерни математичних заблуждень"""
        return {
            MisconceptionType.EQUATION_AS_STATEMENT: {
                "triggers": [
                    "treats_equation_as_calculation",
                    "ignores_equals_sign_meaning",
                    "performs_operations_left_to_right_only"
                ],
                "symptoms": [
                    "Розв'язує ліву частину як окремий приклад",
                    "Не розуміє, що обидві частини мають бути рівними",
                    "Змінює лише одну частину рівняння"
                ],
                "typical_errors": [
                    "2x + 3 = 7 → обчислює 2x + 3 = 5x замість виділення x"
                ]
            },
            
            MisconceptionType.OPERATION_REVERSAL: {
                "triggers": [
                    "uses_same_operation_both_sides",
                    "adds_instead_of_subtract",
                    "multiplies_instead_of_divide"
                ],
                "symptoms": [
                    "Використовує ту саму операцію для 'скасування'",
                    "Додає число замість віднімання",
                    "Множить замість ділення"
                ],
                "typical_errors": [
                    "x + 5 = 10 → x + 5 + 5 = 10 + 5 (додає замість віднімання)",
                    "3x = 12 → 3x × 3 = 12 × 3 (множить замість ділення)"
                ]
            },
            
            MisconceptionType.SIGN_ERROR: {
                "triggers": [
                    "wrong_sign_choice",
                    "loses_negative_signs",
                    "double_negative_confusion"
                ],
                "symptoms": [
                    "Плутає + і - при перенесенні",
                    "Втрачає від'ємні знаки",
                    "Неправильно обробляє подвійні негативи"
                ],
                "typical_errors": [
                    "x - 3 = 7 → x - 3 - 3 = 7 - 3 (віднімає замість додавання)",
                    "x + (-5) = 2 → плутається з операцією"
                ]
            },
            
            MisconceptionType.COEFFICIENT_CONFUSION: {
                "triggers": [
                    "treats_coefficient_as_separate",
                    "adds_to_coefficient_instead_divide",
                    "ignores_coefficient"
                ],
                "symptoms": [
                    "2x розглядає як 2 + x",
                    "Намагається 'прибрати' коефіцієнт додаванням/відніманням",
                    "Ігнорує коефіцієнт при обчисленнях"
                ],
                "typical_errors": [
                    "2x = 8 → 2x - 2 = 8 - 2 (намагається відняти коефіцієнт)",
                    "5x = 20 → x = 20 (ігнорує коефіцієнт 5)"
                ]
            },
            
            MisconceptionType.BALANCE_VIOLATION: {
                "triggers": [
                    "changes_only_one_side",
                    "different_operations_each_side",
                    "ignores_equality_principle"
                ],
                "symptoms": [
                    "Змінює тільки ліву або праву частину",
                    "Робить різні операції з різними боками",
                    "Не розуміє принцип збереження рівності"
                ],
                "typical_errors": [
                    "x + 3 = 7 → x = 7 (прибирає 3 тільки зліва)",
                    "2x = 6 → x = 6 ÷ 2 (ділить тільки праву частину)"
                ]
            }
        }
    
    def _initialize_remediation(self) -> Dict[MisconceptionType, Dict]:
        """Стратегії виправлення для кожного типу помилки"""
        return {
            MisconceptionType.EQUATION_AS_STATEMENT: {
                "primary_strategy": "balance_metaphor",
                "interventions": [
                    "Показати рівняння як ваги",
                    "Підкреслити значення знака =",
                    "Практика з конкретними предметами"
                ],
                "visual_aids": ["balance_scale", "see_saw", "equal_groups"],
                "practice_problems": "simple_balance_equations"
            },
            
            MisconceptionType.OPERATION_REVERSAL: {
                "primary_strategy": "inverse_operation_pairs",
                "interventions": [
                    "Таблиця операцій та їх оберненості",
                    "Демонстрація 'скасування' операцій",
                    "Аналогії з реальним життям"
                ],
                "visual_aids": ["operation_pairs_chart", "cancellation_animation"],
                "practice_problems": "inverse_operation_drills"
            },
            
            MisconceptionType.SIGN_ERROR: {
                "primary_strategy": "sign_tracking",
                "interventions": [
                    "Кольорове кодування знаків",
                    "Покрокове відстеження знаків",
                    "Правила перенесення через знак ="
                ],
                "visual_aids": ["color_coded_signs", "sign_flip_animation"],
                "practice_problems": "sign_focused_equations"
            },
            
            MisconceptionType.COEFFICIENT_CONFUSION: {
                "primary_strategy": "coefficient_meaning",
                "interventions": [
                    "Пояснення 2x як '2 групи по x'",
                    "Візуальне представлення множення",
                    "Практика з конкретними числами"
                ],
                "visual_aids": ["grouped_objects", "multiplication_arrays"],
                "practice_problems": "coefficient_meaning_problems"
            },
            
            MisconceptionType.BALANCE_VIOLATION: {
                "primary_strategy": "equality_preservation",
                "interventions": [
                    "Акцент на 'те саме з обох боків'",
                    "Фізичні ваги з реальними предметами",
                    "Перевірка рівності після кожного кроку"
                ],
                "visual_aids": ["physical_balance", "equality_check_marks"],
                "practice_problems": "balance_preservation_drills"
            }
        }
    
    def analyze_student_error(self, correct_operation: str, chosen_operation: str, 
                            equation_context: Dict, student_history: Dict) -> List[ErrorPattern]:
        """Аналізує помилку студента та повертає можливі заблуждення"""
        
        detected_patterns = []
        
        # Аналіз операції
        operation_analysis = self._analyze_operation_choice(correct_operation, chosen_operation)
        
        # Аналіз контексту рівняння
        context_analysis = self._analyze_equation_context(equation_context, chosen_operation)
        
        # Аналіз історії помилок
        history_analysis = self._analyze_error_history(student_history, chosen_operation)
        
        # Комбінуємо всі аналізи
        all_indicators = {**operation_analysis, **context_analysis, **history_analysis}
        
        # Визначаємо найбільш ймовірні заблуждення
        for misconception, pattern_data in self.misconception_patterns.items():
            confidence = self._calculate_misconception_confidence(
                all_indicators, pattern_data, student_history
            )
            
            if confidence > 0.3:  # Поріг для включення в список
                detected_patterns.append(ErrorPattern(
                    misconception_type=misconception,
                    confidence=confidence,
                    evidence=self._collect_evidence(all_indicators, pattern_data),
                    frequency=student_history.get('error_patterns', {}).get(misconception.value, 0),
                    severity=self._calculate_severity(misconception, confidence, student_history)
                ))
        
        # Сортуємо за впевненістю
        detected_patterns.sort(key=lambda x: x.confidence, reverse=True)
        
        return detected_patterns[:3]  # Повертаємо топ-3 найбільш ймовірних
    
    def _analyze_operation_choice(self, correct: str, chosen: str) -> Dict[str, Any]:
        """Аналізує вибір операції"""
        indicators = {}
        
        # Витягуємо операцію та число
        correct_match = re.match(r'([+\-*/]) (\d+)', correct)
        chosen_match = re.match(r'([+\-*/]) (\d+)', chosen)
        
        if correct_match and chosen_match:
            correct_op, correct_num = correct_match.groups()
            chosen_op, chosen_num = chosen_match.groups()
            
            # Перевіряємо тип помилки
            if correct_op != chosen_op:
                if (correct_op == '-' and chosen_op == '+') or (correct_op == '+' and chosen_op == '-'):
                    indicators['sign_reversal'] = True
                elif (correct_op == '*' and chosen_op == '/') or (correct_op == '/' and chosen_op == '*'):
                    indicators['inverse_confusion'] = True
                elif correct_op in ['-', '/'] and chosen_op in ['+', '*']:
                    indicators['operation_reversal'] = True
            
            if correct_num != chosen_num:
                indicators['wrong_number'] = True
        
        return indicators
    
    def _analyze_equation_context(self, context: Dict, chosen_operation: str) -> Dict[str, Any]:
        """Аналізує контекст рівняння для виявлення заблуждень"""
        indicators = {}
        
        equation_parts = context.get('equation_parts', {})
        a, b, c = equation_parts.get('a', 1), equation_parts.get('b', 0), equation_parts.get('c', 0)
        
        # Перевіряємо, чи студент розуміє структуру рівняння
        if 'current_step' in context:
            step = context['current_step']
            if step == 0 and b != 0:  # Перший крок має прибрати константу
                if '+ ' in chosen_operation and b > 0:
                    indicators['adds_instead_of_subtract'] = True
                elif '- ' in chosen_operation and b < 0:
                    indicators['subtracts_negative_wrong'] = True
            
            elif step == 1 and a != 1:  # Другий крок має прибрати коефіцієнт
                if '+ ' in chosen_operation or '- ' in chosen_operation:
                    indicators['treats_coefficient_as_addend'] = True
        
        return indicators
    
    def _analyze_error_history(self, history: Dict, chosen_operation: str) -> Dict[str, Any]:
        """Аналізує історію помилок для виявлення паттернів"""
        indicators = {}
        
        error_patterns = history.get('error_patterns', {})
        
        # Перевіряємо повторювані помилки
        for error_type, count in error_patterns.items():
            if count >= 2:
                indicators[f'recurring_{error_type}'] = True
        
        # Аналізуємо загальну тенденцію
        total_attempts = history.get('total_attempts', 1)
        consecutive_correct = history.get('consecutive_correct', 0)
        
        if consecutive_correct == 0 and total_attempts > 3:
            indicators['persistent_confusion'] = True
        
        return indicators
    
    def _calculate_misconception_confidence(self, indicators: Dict, pattern_data: Dict, 
                                         history: Dict) -> float:
        """Обчислює впевненість у конкретному заблудженні"""
        base_confidence = 0.0
        
        # Перевіряємо тригери
        triggers = pattern_data.get('triggers', [])
        triggered_count = sum(1 for trigger in triggers if indicators.get(trigger, False))
        
        if triggered_count > 0:
            base_confidence = triggered_count / len(triggers)
        
        # Додаємо бонус за історію
        error_patterns = history.get('error_patterns', {})
        if any(pattern in error_patterns for pattern in triggers):
            base_confidence += 0.2
        
        # Штраф за суперечливі індикатори
        conflicting_indicators = 0
        for indicator in indicators:
            if indicator not in triggers and indicators[indicator]:
                conflicting_indicators += 1
        
        if conflicting_indicators > 2:
            base_confidence *= 0.7
        
        return min(1.0, base_confidence)
    
    def _collect_evidence(self, indicators: Dict, pattern_data: Dict) -> List[str]:
        """Збирає докази для конкретного заблуждення"""
        evidence = []
        
        triggers = pattern_data.get('triggers', [])
        for trigger in triggers:
            if indicators.get(trigger, False):
                evidence.append(f"Виявлено: {trigger}")
        
        symptoms = pattern_data.get('symptoms', [])
        for i, trigger in enumerate(triggers):
            if indicators.get(trigger, False) and i < len(symptoms):
                evidence.append(symptoms[i])
        
        return evidence
    
    def _calculate_severity(self, misconception: MisconceptionType, 
                          confidence: float, history: Dict) -> float:
        """Обчислює серйозність заблуждення для навчального процесу"""
        
        # Базова серйозність залежно від типу
        base_severity = {
            MisconceptionType.EQUATION_AS_STATEMENT: 0.9,      # Критично важливо
            MisconceptionType.BALANCE_VIOLATION: 0.9,          # Критично важливо
            MisconceptionType.OPERATION_REVERSAL: 0.7,         # Дуже важливо
            MisconceptionType.COEFFICIENT_CONFUSION: 0.7,      # Дуже важливо
            MisconceptionType.SIGN_ERROR: 0.5,                 # Важливо
            MisconceptionType.VARIABLE_MISCONCEPTION: 0.8,     # Дуже важливо
            MisconceptionType.ORDER_OF_OPERATIONS: 0.6,        # Важливо
            MisconceptionType.PROCEDURAL_ERROR: 0.3            # Менш критично
        }.get(misconception, 0.5)
        
        # Збільшуємо серйозність при повторних помилках
        frequency = history.get('error_patterns', {}).get(misconception.value, 0)
        frequency_multiplier = min(1.5, 1.0 + frequency * 0.1)
        
        # Обчислюємо фінальну серйозність
        final_severity = base_severity * confidence * frequency_multiplier
        
        return min(1.0, final_severity)

class PersonalizedRemediation:
    """Система персоналізованого виправлення помилок"""
    
    def __init__(self):
        self.remediation_database = self._initialize_remediation_db()
    
    def _initialize_remediation_db(self) -> Dict[MisconceptionType, Dict]:
        """База даних стратегій виправлення"""
        return {
            MisconceptionType.EQUATION_AS_STATEMENT: {
                "visual_explanations": [
                    "Покажіть рівняння 2x + 3 = 7 як ваги: ліва чаша важить 2x+3, права 7",
                    "Підкресліть: знак = означає 'однакова вага', не 'обчислити'"
                ],
                "analogies": [
                    "Рівняння - це як ваги в магазині: обидві чаші мають важити однаково",
                    "Уявіть гойдалку: вона буде рівноважити, тільки якщо з обох боків однакова вага"
                ],
                "practice_sequence": [
                    "Почніть з простих рівнянь типу x + 3 = 5",
                    "Завжди перевіряйте відповідь, підставляючи назад"
                ]
            },
            
            MisconceptionType.OPERATION_REVERSAL: {
                "visual_explanations": [
                    "Покажіть таблицю: + скасовується -, × скасовується ÷",
                    "Демонстрація: якщо додали 5, то щоб повернутись, треба відняти 5"
                ],
                "analogies": [
                    "Як кроки: якщо зробили 3 кроки вперед, треба 3 кроки назад",
                    "Як одягання: якщо одягли светр, щоб зняти - треба роздягнути"
                ],
                "practice_sequence": [
                    "Практика з простими 'відміна' діями",
                    "x + 5 = 8: що треба зробити, щоб 'прибрати' +5?"
                ]
            }
        }
    
    def generate_personalized_help(self, error_patterns: List[ErrorPattern], 
                                 student_profile: Dict) -> Dict[str, Any]:
        """Генерує персоналізовану допомогу на основі помилок"""
        
        if not error_patterns:
            return {"message": "Спробуйте ще раз, уважно прочитавши умову"}
        
        primary_error = error_patterns[0]  # Найбільш ймовірна помилка
        misconception = primary_error.misconception_type
        
        # Отримуємо стратегії для цього типу помилки
        strategies = self.remediation_database.get(misconception, {})
        
        # Адаптуємо під профіль студента
        learning_style = student_profile.get('learning_style', 'visual')
        
        help_content = {
            "primary_issue": misconception.value,
            "confidence": primary_error.confidence,
            "explanation": self._select_explanation(strategies, learning_style),
            "analogy": self._select_analogy(strategies, learning_style),
            "practice_tip": self._select_practice_tip(strategies, primary_error.frequency),
            "visual_aid": self._recommend_visual_aid(misconception, learning_style),
            "encouragement": self._generate_encouragement(primary_error.frequency)
        }
        
        return help_content
    
    def _select_explanation(self, strategies: Dict, learning_style: str) -> str:
        """Вибирає найкраще пояснення для стилю навчання"""
        explanations = strategies.get('visual_explanations', ['Спробуйте ще раз'])
        
        if learning_style == 'visual' and explanations:
            return explanations[0]
        elif len(explanations) > 1:
            return explanations[1]
        else:
            return explanations[0] if explanations else "Перечитайте умову уважно"
    
    def _select_analogy(self, strategies: Dict, learning_style: str) -> str:
        """Вибирає аналогію"""
        analogies = strategies.get('analogies', [])
        return analogies[0] if analogies else ""
    
    def _select_practice_tip(self, strategies: Dict, error_frequency: int) -> str:
        """Вибирає практичну пораду"""
        tips = strategies.get('practice_sequence', [])
        
        if error_frequency >= 3 and len(tips) > 1:
            return tips[1]  # Більш докладна порада для повторних помилок
        elif tips:
            return tips[0]
        else:
            return "Практикуйтесь з простішими прикладами"
    
    def _recommend_visual_aid(self, misconception: MisconceptionType, 
                            learning_style: str) -> str:
        """Рекомендує візуальну допомогу"""
        visual_aids = {
            MisconceptionType.EQUATION_AS_STATEMENT: "balance_scale_animation",
            MisconceptionType.OPERATION_REVERSAL: "inverse_operations_chart",
            MisconceptionType.BALANCE_VIOLATION: "equality_preservation_demo",
            MisconceptionType.SIGN_ERROR: "sign_tracking_colors"
        }
        
        return visual_aids.get(misconception, "step_by_step_guide")
    
    def _generate_encouragement(self, frequency: int) -> str:
        """Генерує підбадьорення"""
        if frequency == 0:
            return "Це нормально - всі роблять помилки під час навчання!"
        elif frequency <= 2:
            return "Ви на правильному шляху. Ця помилка допоможе краще зрозуміти концепцію."
        else:
            return "Цей тип задач потребує більше практики. Спробуємо інший підхід."