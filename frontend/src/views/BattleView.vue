<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '@/services/api'
import ProgressiveAlgebra from '@/components/ProgressiveAlgebra.vue'
import InteractiveGeometry from '@/components/InteractiveGeometry.vue'

// --- Стан компонента ---
const battleState = ref(null)
const enemyCurrentHp = ref(0)
const userAnswer = ref('')
const message = ref('')
const isLoading = ref(true)
const isEnemyHit = ref(false)

// Посилання на компонент прогресивної алгебри
const progressiveAlgebraRef = ref(null)

// Нові стани для концептуального навчання
const showConceptHint = ref(false)
const conceptFeedback = ref('')
const mistakeAnalysis = ref('')
const encouragementMessage = ref('')

// Компоненти
const components = {
  ProgressiveAlgebra,
  InteractiveGeometry,
}

// --- Computed властивості ---
const isVictory = computed(() => enemyCurrentHp.value <= 0 && battleState.value !== null)
const isDefeat = computed(() => battleState.value && battleState.value.player_stats.hp <= 0)
const isBattleOver = computed(() => isVictory.value || isDefeat.value)

// Отримуємо концептуальну інформацію з поточної задачі
const conceptInfo = computed(() => {
  if (!battleState.value?.problem?.data) return null

  return {
    context: battleState.value.problem.data.context || 'basic',
    hint: battleState.value.problem.data.concept_hint || '',
    explanation: battleState.value.problem.data.context_explanation || '',
    difficulty: battleState.value.problem.data.difficulty_factors || {},
  }
})

// Додаємо computed properties для Геометричного Титана
const isGeometricTitan = computed(
  () =>
    battleState.value?.enemy?.name?.toLowerCase().includes('geometric') ||
    battleState.value?.enemy?.name?.toLowerCase().includes('gargoyle'),
)

const getCurrentTitanForm = computed(() => {
  if (!battleState.value?.problem?.data?.shape) return 'Невідома'

  const shapeType = battleState.value.problem.data.shape.type
  const forms = {
    rectangle: 'Прямокутна Фортеця',
    circle: 'Кристалічна Сфера',
    triangle: 'Піраміда Влади',
  }

  return forms[shapeType] || 'Абстрактна Форма'
})

// --- Функції ---
const startNewBattle = async () => {
  isLoading.value = true
  try {
    const response = await api.startBattle()
    battleState.value = response.data
    enemyCurrentHp.value = response.data.enemy.max_hp
    message.value = `Ворог з'явився! Розв'яжіть задачу, щоб атакувати.`

    // Очищуємо попередні повідомлення
    conceptFeedback.value = ''
    mistakeAnalysis.value = ''
    encouragementMessage.value = ''
  } catch (error) {
    message.value = 'Не вдалося почати бій. Спробуйте оновити сторінку.'
    console.error('Battle start error:', error)
  } finally {
    isLoading.value = false
  }
}

const toggleConceptHint = () => {
  showConceptHint.value = !showConceptHint.value
}

onMounted(startNewBattle)

// Функція для обробки прогресивної алгебри
const handleAlgebraOperation = (operation) => {
  submitTurn({ operation })
}

const handleEquationCompleted = () => {
  // Рівняння розв'язано - завдаємо шкоди ворогу
  const damageDealt = 30 // Бонусна шкода за завершення рівняння
  enemyCurrentHp.value = Math.max(0, enemyCurrentHp.value - damageDealt)

  message.value = `Рівняння розв'язано! Завдано ${damageDealt} шкоди ворогу.`

  // Анімація удару
  isEnemyHit.value = true
  setTimeout(() => {
    isEnemyHit.value = false
  }, 300)
}

const handleNextStep = () => {
  // Просто оновлюємо інтерфейс для наступного кроку
  // Логіка переходів вже в прогресивному компоненті
}

// Нові методи для обробки геометричних відповідей
const handleGeometryAnswer = (answerData) => {
  submitTurn({
    answer: answerData.answer,
    problemType: 'geometry',
    challengeType: answerData.challengeType,
  })
}

const handleGeometrySolution = (solutionData) => {
  // Геометричну задачу завершено успішно
  const damageDealt = solutionData.damage || 25
  enemyCurrentHp.value = Math.max(0, enemyCurrentHp.value - damageDealt)

  message.value = `Геометричне заклинання завдало ${damageDealt} шкоди! ${solutionData.encouragement || ''}`

  // Анімація удару
  isEnemyHit.value = true
  setTimeout(() => {
    isEnemyHit.value = false
  }, 300)

  // Перевірка перемоги
  if (enemyCurrentHp.value <= 0) {
    message.value = `Геометричний Титан переможений! Ви отримали ${solutionData.xp || 20} досвіду.`

    // Оновлюємо XP гравця
    if (battleState.value?.player_stats) {
      battleState.value.player_stats.xp += solutionData.xp || 20
    }
  } else {
    // Генеруємо нову задачу після короткої затримки
    setTimeout(async () => {
      try {
        const response = await api.startBattle()
        battleState.value.problem = response.data.problem
        message.value = "Геометричний Титан трансформується! Нова геометрична форма з'явилась."
      } catch (error) {
        console.error('Помилка генерації нової задачі:', error)
      }
    }, 2000)
  }
}

// Допоміжна функція для отримання всіх варіантів операцій (алгебра)
const getAvailableOperations = computed(() => {
  if (!battleState.value?.problem?.data?.type === 'equation') return []

  const problemData = battleState.value.problem.data
  const currentIndex = problemData.current_step_index || 0
  const steps = problemData.solution_steps || []

  if (currentIndex >= steps.length) return []

  const currentStep = steps[currentIndex]
  const wrongOptions = currentStep.wrong_options || []

  const allOptions = [
    {
      operation: currentStep.operation,
      description: currentStep.description,
      correct: true,
    },
    ...wrongOptions,
  ]

  return allOptions.sort(() => Math.random() - 0.5)
})

// Універсальна функція для обробки відповідей з покращеним фідбеком
const submitTurn = async ({ answer, operation, problemType, challengeType } = {}) => {
  if (!battleState.value || isBattleOver.value) return

  try {
    const response = await api.submitAnswer(
      battleState.value.enemy.id,
      battleState.value.problem,
      answer,
      operation,
    )

    const result = response.data

    // Завжди оновлюємо статистику гравця
    battleState.value.player_stats = result.new_player_stats

    // Завжди оновлюємо задачу, якщо вона є
    if (result.new_problem) {
      battleState.value.problem = result.new_problem
    }

    // Оновлюємо фідбек від сервера
    if (result.feedback_message) {
      message.value = result.feedback_message
    }

    if (result.concept_reinforcement) {
      conceptFeedback.value = result.concept_reinforcement
    }

    if (result.mistake_analysis) {
      mistakeAnalysis.value = result.mistake_analysis
    }

    if (result.encouragement) {
      encouragementMessage.value = result.encouragement
    }

    if (result.is_correct) {
      const problemType = battleState.value.problem.data?.type
      const isEquationSolved =
        problemType === 'equation' && battleState.value.problem.data?.equation_parts?.x_isolated

      if (problemType === 'progressive_equation') {
        // Передаємо результат у прогресивний компонент
        if (progressiveAlgebraRef.value) {
          progressiveAlgebraRef.value.showOperationResult(result)
        }

        // Якщо рівняння не завершено, не завдаємо шкоди
        if (!result.is_equation_solved) {
          conceptFeedback.value = result.feedback || "Правильно! Продовжуємо розв'язання."
        } else {
          // Рівняння завершено - завдаємо шкоди
          const damageDealt = result.damage_dealt || 30
          enemyCurrentHp.value = Math.max(0, enemyCurrentHp.value - damageDealt)

          isEnemyHit.value = true
          setTimeout(() => {
            isEnemyHit.value = false
          }, 300)
        }
      } else if (problemType === 'equation' && !isEquationSolved) {
        // Алгебра в процесі
        conceptFeedback.value = 'Правильно! Рівняння спрощується.'
      } else {
        // Завдаємо шкоду ворогу ЗАВЖДИ при правильній відповіді
        const damageDealt = result.damage_dealt || 0
        if (damageDealt > 0) {
          enemyCurrentHp.value = Math.max(0, enemyCurrentHp.value - damageDealt)

          // Анімація удару
          isEnemyHit.value = true
          setTimeout(() => {
            isEnemyHit.value = false
          }, 300)
        }
      }
    }

    // Перевіряємо кінець бою
    if (enemyCurrentHp.value <= 0) {
      message.value = `Перемога! Ви отримали ${result.xp_gained} досвіду.`
    } else if (battleState.value.player_stats.hp <= 0) {
      message.value = 'Поразка... Спробуйте ще раз.'
    }
  } catch (error) {
    message.value = 'Помилка при відправці відповіді.'
    console.error('Submit turn error:', error)
  } finally {
    userAnswer.value = ''
  }
}
</script>

<template>
  <div class="battle-view">
    <div v-if="isLoading" class="loading">Завантаження бою...</div>

    <div v-else-if="battleState" class="battle-arena">
      <!-- Статистика гравця -->
      <div class="player-stats card" :class="{ defeated: isDefeat }">
        <h2>
          {{ battleState.player_stats.owner.username }} (Рівень
          {{ battleState.player_stats.level }})
        </h2>
        <p>HP: {{ battleState.player_stats.hp }} / {{ battleState.player_stats.max_hp }}</p>
        <p>XP: {{ battleState.player_stats.xp }} / {{ 100 * battleState.player_stats.level }}</p>
        <p>
          <strong>Сила Математики: {{ battleState.player_stats.math_power }}</strong>
        </p>
      </div>

      <!-- Статистика ворога -->
      <div class="enemy-stats card" :class="{ defeated: isVictory }">
        <img
          v-if="battleState.enemy.image_url"
          :src="battleState.enemy.image_url"
          :alt="battleState.enemy.name"
          class="enemy-sprite"
          :class="{ hit: isEnemyHit, 'geometric-transformation': isGeometricTitan }"
        />

        <!-- Спеціальна анімація для Геометричного Титана -->
        <div v-if="isGeometricTitan" class="titan-form-indicator">
          <span class="current-form"> Поточна форма: {{ getCurrentTitanForm }} </span>
        </div>

        <h2>{{ battleState.enemy.name }}</h2>
        <p>HP: {{ enemyCurrentHp }} / {{ battleState.enemy.max_hp }}</p>

        <!-- Показуємо спеціальні здібності для геометричного титана -->
        <div v-if="isGeometricTitan" class="titan-abilities">
          <div class="ability-item">🔄 Трансформація форми</div>
          <div class="ability-item">📐 Геометрична досконалість</div>
        </div>

        <div class="vulnerabilities">
          <p v-if="battleState.enemy.vulnerability" class="vulnerable">
            Вразливість: <strong>{{ battleState.enemy.vulnerability }}</strong>
          </p>
          <p v-if="battleState.enemy.resistance" class="resistant">
            Опір: <strong>{{ battleState.enemy.resistance }}</strong>
          </p>
        </div>
      </div>

      <!-- Область задачі -->
      <div class="problem-area card">
        <div v-if="isVictory">
          <h2>Перемога!</h2>
          <p v-if="encouragementMessage" class="encouragement">{{ encouragementMessage }}</p>
          <button @click="startNewBattle" class="victory-button">Почати новий бій</button>
        </div>
        <div v-else-if="isDefeat">
          <h2>Поразка...</h2>
          <p v-if="mistakeAnalysis" class="mistake-analysis">{{ mistakeAnalysis }}</p>
          <router-link to="/sanctum" class="return-button">Повернутися у Святилище</router-link>
        </div>
        <div v-else>
          <!-- Заголовок з кнопкою підказки -->
          <div class="problem-header">
            <h2>Задача:</h2>
            <button
              v-if="conceptInfo?.hint"
              @click="toggleConceptHint"
              class="hint-button"
              :class="{ active: showConceptHint }"
            >
              💡 {{ showConceptHint ? 'Сховати підказку' : 'Показати підказку' }}
            </button>
          </div>

          <!-- Концептуальна підказка -->
          <div v-if="showConceptHint && conceptInfo?.hint" class="concept-hint">
            <div class="hint-content">
              <p><strong>Підказка:</strong> {{ conceptInfo.hint }}</p>
              <p v-if="conceptInfo.explanation">
                <strong>Пояснення:</strong> {{ conceptInfo.explanation }}
              </p>
            </div>
          </div>

          <!-- Текст задачі -->
          <p class="problem-text">
            {{ battleState.problem.display_text }}
            <span
              v-if="!battleState.problem.data?.type || battleState.problem.data.type !== 'equation'"
            >
              = ?
            </span>
          </p>

          <!-- Візуалізація для геометрії -->
          <div v-if="battleState.problem.data?.shape === 'rectangle'" class="problem-visualization">
            <p class="visualization-title">Візуальна умова:</p>
            <div class="greybox-rectangle">
              <span class="height-label">{{ battleState.problem.data.height }}</span>
              <span class="width-label">{{ battleState.problem.data.width }}</span>
            </div>
          </div>

          <!-- Прогресивна алгебра -->
          <div v-if="battleState.problem.data?.type === 'progressive_equation'">
            <ProgressiveAlgebra
              ref="progressiveAlgebraRef"
              :problem-data="battleState.problem.data"
              @operation-selected="handleAlgebraOperation"
              @equation-completed="handleEquationCompleted"
              @next-step="handleNextStep"
            />
          </div>

          <!-- Інтерактивна геометрія -->
          <div v-else-if="battleState.problem.data?.type === 'geometry'">
            <InteractiveGeometry
              :problem-data="battleState.problem"
              @answer-submitted="handleGeometryAnswer"
              @solution-completed="handleGeometrySolution"
            />
          </div>

          <!-- Стара алгебра (fallback) -->
          <div v-else-if="battleState.problem.data?.type === 'equation'">
            <div class="equation-container">
              <span v-if="battleState.problem.data.equation_parts.a !== 1">
                {{ battleState.problem.data.equation_parts.a }}
              </span>
              <span v-if="!battleState.problem.data.equation_parts.x_isolated">x</span>
              <span v-if="battleState.problem.data.equation_parts.b > 0" class="equation-operator"
                >+</span
              >
              <span v-if="battleState.problem.data.equation_parts.b < 0" class="equation-operator"
                >-</span
              >
              <span v-if="battleState.problem.data.equation_parts.b !== 0">
                {{ Math.abs(battleState.problem.data.equation_parts.b) }}
              </span>
              <span class="equation-operator"> = </span>
              <span>{{ battleState.problem.data.equation_parts.c }}</span>
            </div>

            <div
              v-if="
                !battleState.problem.data.equation_parts.x_isolated &&
                getAvailableOperations.length > 0
              "
              class="operations-grid"
            >
              <button
                v-for="option in getAvailableOperations"
                :key="option.operation"
                @click="submitTurn({ operation: option.operation })"
                class="operation-button"
              >
                {{ option.description }}
              </button>
            </div>

            <div
              v-else-if="battleState.problem.data.equation_parts.x_isolated"
              class="solved-message"
            >
              Рівняння розв'язане! x = {{ battleState.problem.answer }}
            </div>
          </div>

          <!-- Форма для числових відповідей -->
          <form v-else @submit.prevent="submitTurn({ answer: parseInt(userAnswer) })">
            <input type="number" v-model="userAnswer" placeholder="Ваша відповідь" required />
            <button type="submit">Атакувати</button>
          </form>
        </div>
      </div>

      <!-- Область повідомлень з розширеним фідбеком -->
      <div class="message-log card">
        <div class="main-message">
          <p>{{ message }}</p>
        </div>

        <!-- Концептуальний фідбек -->
        <div v-if="conceptFeedback" class="concept-feedback">
          <h4>🔮 Магічне розуміння:</h4>
          <p>{{ conceptFeedback }}</p>
        </div>

        <!-- Аналіз помилки -->
        <div v-if="mistakeAnalysis" class="mistake-feedback">
          <h4>📚 Підказка майстра:</h4>
          <p>{{ mistakeAnalysis }}</p>
        </div>

        <!-- Підбадьорення -->
        <div v-if="encouragementMessage" class="encouragement-feedback">
          <h4>⭐ Досягнення:</h4>
          <p>{{ encouragementMessage }}</p>
        </div>
      </div>
    </div>

    <div v-else>
      <p>{{ message }}</p>
    </div>
  </div>
</template>

<style scoped>
.battle-view {
  padding: 2rem;
}

.loading {
  text-align: center;
  font-size: 1.5rem;
  padding: 2rem;
}

.battle-arena {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  max-width: 900px;
  margin: auto;
}

.card {
  padding: 1.5rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

.problem-area,
.message-log {
  grid-column: 1 / -1;
  text-align: center;
}

.problem-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.hint-button {
  padding: 0.5rem 1rem;
  background-color: #f0f8ff;
  border: 2px solid #4a90e2;
  border-radius: 6px;
  color: #4a90e2;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.hint-button:hover,
.hint-button.active {
  background-color: #4a90e2;
  color: white;
}

.concept-hint {
  background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
  border: 2px solid #4a90e2;
  border-radius: 12px;
  padding: 1.5rem;
  margin: 1rem 0;
  text-align: left;
}

.hint-content p {
  margin: 0.5rem 0;
  color: #2c3e50;
}

.problem-text {
  font-size: 1.8rem;
  font-weight: bold;
  margin: 1rem 0;
  color: #333;
  line-height: 1.4;
}

.concept-feedback {
  background: linear-gradient(135deg, #e8f5e8 0%, #f0fff0 100%);
  border-left: 4px solid #28a745;
  padding: 1rem;
  margin-top: 1rem;
  text-align: left;
}

.mistake-feedback {
  background: linear-gradient(135deg, #fff3cd 0%, #fefefe 100%);
  border-left: 4px solid #ffc107;
  padding: 1rem;
  margin-top: 1rem;
  text-align: left;
}

.encouragement-feedback {
  background: linear-gradient(135deg, #e1ecf4 0%, #f8f9ff 100%);
  border-left: 4px solid #7b68ee;
  padding: 1rem;
  margin-top: 1rem;
  text-align: left;
}

.concept-feedback h4,
.mistake-feedback h4,
.encouragement-feedback h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
}

.concept-feedback p,
.mistake-feedback p,
.encouragement-feedback p {
  margin: 0;
  font-size: 0.95rem;
}

/* CSS стилі для анімації титана */
.geometric-transformation {
  animation: titanShift 3s infinite ease-in-out;
}

@keyframes titanShift {
  0%,
  100% {
    transform: scale(1) rotate(0deg);
    filter: hue-rotate(0deg);
  }
  50% {
    transform: scale(1.1) rotate(5deg);
    filter: hue-rotate(30deg);
  }
}

.titan-form-indicator {
  background: rgba(74, 144, 226, 0.2);
  border: 1px solid #4a90e2;
  border-radius: 6px;
  padding: 0.5rem;
  margin: 0.5rem 0;
  font-size: 0.8rem;
  text-align: center;
}

.current-form {
  font-family: 'Orbitron', monospace;
  color: #4a90e2;
  font-weight: bold;
}

.titan-abilities {
  margin: 1rem 0;
  padding: 0.5rem;
  background: rgba(123, 104, 238, 0.1);
  border-radius: 6px;
}

.ability-item {
  font-size: 0.8rem;
  margin: 0.25rem 0;
  color: #7b68ee;
}

input {
  padding: 0.5rem;
  margin-right: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

button {
  padding: 0.5rem 1rem;
  cursor: pointer;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #f8f9fa;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #e9ecef;
}

.victory-button {
  background-color: #28a745;
  color: white;
  border-color: #28a745;
  font-size: 1.1rem;
  padding: 0.75rem 1.5rem;
}

.victory-button:hover {
  background-color: #218838;
}

.return-button {
  display: inline-block;
  padding: 0.5rem 1rem;
  background-color: #6c757d;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.return-button:hover {
  background-color: #5a6268;
}

.defeated {
  opacity: 0.5;
  background-color: #ffdddd;
}

.enemy-sprite {
  max-width: 150px;
  margin: 0 auto 1rem;
  display: block;
  transition: transform 0.1s ease-in-out;
}

.enemy-sprite.hit {
  animation: shake 0.3s;
  filter: brightness(1.5) drop-shadow(0 0 5px red);
}

@keyframes shake {
  0%,
  100% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-5px);
  }
  75% {
    transform: translateX(5px);
  }
}

.problem-visualization {
  margin: 1.5rem auto;
  padding: 1rem;
  border: 1px dashed #555;
  border-radius: 8px;
  max-width: 300px;
}

.visualization-title {
  font-size: 0.9rem;
  color: #888;
  margin-bottom: 1rem;
}

.greybox-rectangle {
  position: relative;
  width: 200px;
  height: 120px;
  border: 2px solid #ccc;
  margin: 1rem auto;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ccc;
}

.height-label {
  position: absolute;
  left: -2rem;
  top: 50%;
  transform: translateY(-50%);
}

.width-label {
  position: absolute;
  bottom: -1.5rem;
  left: 50%;
  transform: translateX(-50%);
}

.equation-container {
  font-size: 2.5rem;
  font-family: 'Orbitron', 'Courier New', monospace;
  margin: 2rem 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: #333;
  flex-wrap: wrap;
}

.equation-operator {
  margin: 0 0.25rem;
}

.operations-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-top: 1.5rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.operation-button {
  border: 2px solid #444;
  background-color: #222;
  color: #eee;
  padding: 1rem 1.5rem;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
  border-radius: 6px;
  text-align: center;
  min-height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.operation-button:hover {
  background-color: #3498db;
  color: #fff;
  border-color: #3498db;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.solved-message {
  color: #28a745;
  font-size: 1.5rem;
  font-weight: bold;
  margin-top: 1.5rem;
}

.vulnerabilities {
  margin-top: 1rem;
  font-size: 0.9rem;
  text-align: left;
  border-top: 1px solid #eee;
  padding-top: 1rem;
}

.vulnerabilities p {
  margin: 0.25rem 0;
}

.vulnerable {
  color: #dc3545;
}

.resistant {
  color: #007bff;
}
</style>
