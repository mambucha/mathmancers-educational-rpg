<template>
  <div class="interactive-geometry">
    <!-- Заголовок з контекстом -->
    <div class="geometry-header">
      <h3 class="challenge-title">{{ getContextTitle() }}</h3>
      <div class="shape-indicator">
        <span class="shape-badge" :class="`shape-${shapeData.type}`">
          {{ getShapeIcon() }} {{ getShapeLabel() }}
        </span>
      </div>
    </div>

    <!-- Інтерактивна область з фігурою -->
    <div class="visualization-container">
      <svg
        ref="geometrySvg"
        class="geometry-canvas"
        :width="canvasSize.width"
        :height="canvasSize.height"
        viewBox="0 0 400 300"
        @mousemove="handleMouseMove"
        @click="handleCanvasClick"
      >
        <!-- Сітка для кращого сприйняття -->
        <defs>
          <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
            <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#e0e0e0" stroke-width="0.5" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" v-if="showGrid" />

        <!-- Рендеримо фігуру залежно від типу -->
        <g class="shape-group" :class="{ interactive: isInteractive, highlighted: isHighlighted }">
          <!-- Прямокутник -->
          <rect
            v-if="shapeData.type === 'rectangle'"
            :x="shapePosition.x"
            :y="shapePosition.y"
            :width="scaleValue(shapeData.width) * scaleFactor"
            :height="scaleValue(shapeData.height) * scaleFactor"
            class="geometry-shape rectangle"
            :class="{ pulsing: showCalculation }"
          />

          <!-- Коло -->
          <circle
            v-else-if="shapeData.type === 'circle'"
            :cx="shapePosition.x + scaleValue(shapeData.radius) * scaleFactor"
            :cy="shapePosition.y + scaleValue(shapeData.radius) * scaleFactor"
            :r="scaleValue(shapeData.radius) * scaleFactor"
            class="geometry-shape circle"
            :class="{ pulsing: showCalculation }"
          />

          <!-- Трикутник -->
          <polygon
            v-else-if="shapeData.type === 'triangle'"
            :points="getTrianglePoints()"
            class="geometry-shape triangle"
            :class="{ pulsing: showCalculation }"
          />
        </g>

        <!-- Підписи розмірів -->
        <g class="dimension-labels" v-if="showDimensions">
          <g v-if="shapeData.type === 'rectangle'">
            <!-- Ширина -->
            <line
              :x1="shapePosition.x"
              :y1="shapePosition.y - 15"
              :x2="shapePosition.x + scaleValue(shapeData.width) * scaleFactor"
              :y2="shapePosition.y - 15"
              class="dimension-line"
            />
            <text
              :x="shapePosition.x + (scaleValue(shapeData.width) * scaleFactor) / 2"
              :y="shapePosition.y - 20"
              class="dimension-text"
              text-anchor="middle"
            >
              {{ shapeData.width }}
            </text>

            <!-- Висота -->
            <line
              :x1="shapePosition.x - 15"
              :y1="shapePosition.y"
              :x2="shapePosition.x - 15"
              :y2="shapePosition.y + scaleValue(shapeData.height) * scaleFactor"
              class="dimension-line"
            />
            <text
              :x="shapePosition.x - 25"
              :y="shapePosition.y + (scaleValue(shapeData.height) * scaleFactor) / 2"
              class="dimension-text"
              text-anchor="middle"
              transform="rotate(-90, this.x, this.y)"
            >
              {{ shapeData.height }}
            </text>
          </g>

          <g v-else-if="shapeData.type === 'circle'">
            <!-- Радіус -->
            <line
              :x1="shapePosition.x + scaleValue(shapeData.radius) * scaleFactor"
              :y1="shapePosition.y + scaleValue(shapeData.radius) * scaleFactor"
              :x2="shapePosition.x + scaleValue(shapeData.radius) * scaleFactor * 2"
              :y2="shapePosition.y + scaleValue(shapeData.radius) * scaleFactor"
              class="dimension-line radius-line"
            />
            <text
              :x="shapePosition.x + scaleValue(shapeData.radius) * scaleFactor * 1.5"
              :y="shapePosition.y + scaleValue(shapeData.radius) * scaleFactor + 5"
              class="dimension-text"
              text-anchor="middle"
            >
              r = {{ shapeData.radius }}
            </text>
          </g>
        </g>

        <!-- Анімовані підказки -->
        <g class="hint-overlay" v-if="showHints && currentHint">
          <foreignObject x="10" y="10" width="380" height="60">
            <div class="hint-bubble">
              <div class="hint-text">{{ currentHint.text }}</div>
              <div class="hint-formula" v-if="currentHint.formula">{{ currentHint.formula }}</div>
            </div>
          </foreignObject>
        </g>
      </svg>

      <!-- Панель інструментів -->
      <div class="geometry-tools" v-if="interactiveFeatures.manipulatable">
        <div class="tool-group">
          <label class="tool-label">
            <input type="checkbox" v-model="showGrid" class="tool-checkbox" />
            🔲 Показати сітку
          </label>

          <label class="tool-label">
            <input type="checkbox" v-model="showDimensions" class="tool-checkbox" />
            📏 Показати розміри
          </label>

          <label class="tool-label">
            <input type="checkbox" v-model="showHints" class="tool-checkbox" />
            💡 Підказки
          </label>
        </div>

        <div class="calculation-display" v-if="showCalculation">
          <div class="formula-step"><strong>Формула:</strong> {{ getCurrentFormula() }}</div>
          <div class="substitution-step"><strong>Підстановка:</strong> {{ getSubstitution() }}</div>
          <div class="result-step" v-if="calculationResult">
            <strong>Результат:</strong> {{ calculationResult }}
          </div>
        </div>
      </div>
    </div>

    <!-- Область введення відповіді -->
    <div class="answer-section">
      <div class="problem-statement">
        <p>{{ problemData.display_text }}</p>
      </div>

      <div class="answer-input-group">
        <input
          type="number"
          v-model.number="userAnswer"
          class="geometry-answer-input"
          :placeholder="getAnswerPlaceholder()"
          @keyup.enter="submitAnswer"
          :class="{ correct: answerState === 'correct', incorrect: answerState === 'incorrect' }"
        />
        <button
          @click="submitAnswer"
          class="submit-geometry-button"
          :disabled="!userAnswer"
          :class="{ calculating: isCalculating }"
        >
          <span v-if="isCalculating" class="spinner">⟳</span>
          <span v-else>Перевірити</span>
        </button>
      </div>

      <!-- Кнопка демонстрації рішення -->
      <button v-if="showSolutionButton" @click="showStepByStep" class="show-solution-button">
        📚 Показати покрокове рішення
      </button>
    </div>

    <!-- Покрокове рішення -->
    <div v-if="showingSolution" class="step-by-step-solution">
      <h4>📋 Покрокове рішення:</h4>
      <ol class="solution-steps">
        <li
          v-for="(step, index) in solutionSteps"
          :key="index"
          class="solution-step"
          :class="{ current: currentSolutionStep === index }"
        >
          {{ step }}
        </li>
      </ol>
      <button @click="hideSolution" class="close-solution-button">Зрозумів ✓</button>
    </div>

    <!-- Результат та фідбек -->
    <div v-if="showResult" class="geometry-result" :class="resultClass">
      <div class="result-header">
        <h4 v-if="answerState === 'correct'">🎉 Правильно!</h4>
        <h4 v-else>🤔 Спробуйте ще раз</h4>
      </div>

      <div class="result-feedback">
        <p v-if="answerState === 'correct'">{{ storyFeedback.success }}</p>
        <p v-else>{{ storyFeedback.failure }}</p>
      </div>

      <div v-if="contextualHint && answerState === 'incorrect'" class="contextual-hint">
        <strong>💡 Підказка:</strong> {{ contextualHint }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'

const props = defineProps({
  problemData: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['answer-submitted', 'solution-completed'])

// Реактивні дані
const geometrySvg = ref(null)
const userAnswer = ref(null)
const answerState = ref(null) // null, 'correct', 'incorrect'
const showResult = ref(false)
const isCalculating = ref(false)
const showGrid = ref(true)
const showDimensions = ref(true)
const showHints = ref(false)
const showCalculation = ref(false)
const showingSolution = ref(false)
const currentSolutionStep = ref(0)
const isInteractive = ref(false)
const isHighlighted = ref(false)

// Обчислювані властивості
const shapeData = computed(() => props.problemData.data?.shape || {})
const interactiveFeatures = computed(() => props.problemData.data?.interactive_features || {})
const storyFeedback = computed(() => props.problemData.data?.story_feedback || {})
const solutionSteps = computed(() => props.problemData.data?.step_by_step || [])
const challengeType = computed(() => props.problemData.data?.challenge_type || 'area')

const canvasSize = computed(() => ({
  width: 400,
  height: 300,
}))

const scaleFactor = computed(() => {
  // Автоматичне масштабування для кращого відображення
  if (shapeData.value.type === 'rectangle') {
    const maxDimension = Math.max(shapeData.value.width || 1, shapeData.value.height || 1)
    return Math.min(200 / maxDimension, 8)
  } else if (shapeData.value.type === 'circle') {
    return Math.min(80 / (shapeData.value.radius || 1), 6)
  }
  return 3
})

const shapePosition = computed(() => ({
  x: 50,
  y: 50,
}))

const showSolutionButton = computed(
  () => answerState.value === 'incorrect' && solutionSteps.value.length > 0,
)

const resultClass = computed(() => ({
  success: answerState.value === 'correct',
  error: answerState.value === 'incorrect',
}))

const calculationResult = computed(() => {
  if (!showCalculation.value) return null

  if (challengeType.value === 'area') {
    if (shapeData.value.type === 'rectangle') {
      return shapeData.value.width * shapeData.value.height
    } else if (shapeData.value.type === 'circle') {
      return Math.round(Math.PI * Math.pow(shapeData.value.radius, 2) * 100) / 100
    }
  }
  return null
})

const currentHint = computed(() => {
  if (!showHints.value) return null

  const hints = {
    area: {
      rectangle: {
        text: 'Для обчислення площі прямокутника перемножте довжину на ширину',
        formula: 'S = довжина × ширина',
      },
      circle: {
        text: 'Площа кола обчислюється за формулою π×r²',
        formula: 'S = π × r²',
      },
      triangle: {
        text: 'Використайте формулу Герона або ½×основа×висота',
        formula: 'S = √(s(s-a)(s-b)(s-c)), де s = (a+b+c)/2',
      },
    },
    perimeter: {
      rectangle: {
        text: 'Периметр - це сума всіх сторін',
        formula: 'P = 2×(довжина + ширина)',
      },
    },
  }

  return hints[challengeType.value]?.[shapeData.value.type] || null
})

const contextualHint = computed(() => {
  const hints = {
    area: {
      rectangle:
        "Пам'ятайте: площа вимірює, скільки квадратних одиниць поміщається всередині фігури",
      circle: 'Не забудьте помножити радіус сам на себе, а потім на π (≈3.14)',
      triangle: 'Якщо не знаєте висоти, використайте формулу Герона',
    },
    perimeter: {
      rectangle: 'Периметр - це довжина "обведення" навколо фігури',
      triangle: 'Просто додайте всі три сторони разом',
    },
    pythagorean: {
      triangle: 'a² + b² = c², де c завжди найдовша сторона (гіпотенуза)',
    },
  }

  return hints[challengeType.value]?.[shapeData.value.type] || 'Уважно прочитайте умову задачі'
})

// Методи
const scaleValue = (value) => {
  return Number(value) || 1
}

const getContextTitle = () => {
  const context = props.problemData.data?.context || 'geometry'
  const titles = {
    fortress_blueprints: '🏰 Будівництво Фортеці',
    magic_portals: '🌀 Магічні Портали',
    crystal_formations: '💎 Кристалічні Формації',
    enchanted_gardens: '🌺 Зачаровані Сади',
  }
  return titles[context] || '📐 Геометрична Задача'
}

const getShapeIcon = () => {
  const icons = {
    rectangle: '⬛',
    circle: '⭕',
    triangle: '🔺',
  }
  return icons[shapeData.value.type] || '📐'
}

const getShapeLabel = () => {
  const labels = {
    rectangle: 'Прямокутник',
    circle: 'Коло',
    triangle: 'Трикутник',
  }
  return labels[shapeData.value.type] || 'Фігура'
}

const getTrianglePoints = () => {
  if (!shapeData.value.vertices) return '0,0 50,0 25,43.3'

  return shapeData.value.vertices
    .map(
      (vertex) =>
        `${shapePosition.value.x + vertex.x * scaleFactor.value},${shapePosition.value.y + vertex.y * scaleFactor.value}`,
    )
    .join(' ')
}

const getCurrentFormula = () => {
  const formulas = {
    area: {
      rectangle: 'S = довжина × ширина',
      circle: 'S = π × r²',
      triangle: 'S = ½ × основа × висота',
    },
    perimeter: {
      rectangle: 'P = 2 × (довжина + ширина)',
      triangle: 'P = a + b + c',
    },
  }

  return formulas[challengeType.value]?.[shapeData.value.type] || ''
}

const getSubstitution = () => {
  if (challengeType.value === 'area') {
    if (shapeData.value.type === 'rectangle') {
      return `S = ${shapeData.value.width} × ${shapeData.value.height}`
    } else if (shapeData.value.type === 'circle') {
      return `S = 3.14 × ${shapeData.value.radius}²`
    }
  } else if (challengeType.value === 'perimeter') {
    if (shapeData.value.type === 'rectangle') {
      return `P = 2 × (${shapeData.value.width} + ${shapeData.value.height})`
    }
  }
  return ''
}

const getAnswerPlaceholder = () => {
  const placeholders = {
    area: 'Введіть площу',
    perimeter: 'Введіть периметр',
    pythagorean: 'Введіть довжину сторони',
  }
  return placeholders[challengeType.value] || 'Ваша відповідь'
}

// Обробники подій
const handleMouseMove = (event) => {
  if (!interactiveFeatures.value.manipulatable) return

  // Додаткова інтерактивність - підсвічування при наведенні
  const rect = geometrySvg.value.getBoundingClientRect()
  const mouseX = event.clientX - rect.left
  const mouseY = event.clientY - rect.top

  // Простий хітбокс для форм
  isHighlighted.value = isPointInShape(mouseX, mouseY)
}

const handleCanvasClick = (event) => {
  if (!interactiveFeatures.value.manipulatable) return

  // Можливість клікнути для показу/приховання обчислень
  showCalculation.value = !showCalculation.value
}

const isPointInShape = (x, y) => {
  // Спрощена перевірка для демонстрації
  const shapeX = shapePosition.value.x
  const shapeY = shapePosition.value.y

  if (shapeData.value.type === 'rectangle') {
    const width = scaleValue(shapeData.value.width) * scaleFactor.value
    const height = scaleValue(shapeData.value.height) * scaleFactor.value
    return x >= shapeX && x <= shapeX + width && y >= shapeY && y <= shapeY + height
  }

  return false
}

const submitAnswer = async () => {
  if (!userAnswer.value || isCalculating.value) return

  isCalculating.value = true
  showResult.value = false

  // Симулюємо відправку на сервер
  await new Promise((resolve) => setTimeout(resolve, 500))

  const correctAnswer = props.problemData.answer
  const isCorrect = Math.abs(userAnswer.value - correctAnswer) < 1 // Допуск для округлень

  answerState.value = isCorrect ? 'correct' : 'incorrect'
  showResult.value = true
  isCalculating.value = false

  // Емітимо результат для батьківського компонента
  emit('answer-submitted', {
    answer: userAnswer.value,
    isCorrect: isCorrect,
    problemType: 'geometry',
    challengeType: challengeType.value,
  })

  // Якщо правильно - завершуємо через кілька секунд
  if (isCorrect) {
    setTimeout(() => {
      emit('solution-completed', {
        damage: calculateDamage(),
        xp: 15,
        encouragement: storyFeedback.value.success,
      })
    }, 2000)
  }
}

const calculateDamage = () => {
  // Базова шкода залежить від складності
  const baseDamage = 20
  const levelMultiplier = props.problemData.data?.level || 1
  return baseDamage + levelMultiplier * 5
}

const showStepByStep = () => {
  showingSolution.value = true
  currentSolutionStep.value = 0
  animateSolutionSteps()
}

const animateSolutionSteps = () => {
  if (currentSolutionStep.value < solutionSteps.value.length - 1) {
    setTimeout(() => {
      currentSolutionStep.value++
      animateSolutionSteps()
    }, 1500)
  }
}

const hideSolution = () => {
  showingSolution.value = false
  currentSolutionStep.value = 0
}

// Життєвий цикл
onMounted(() => {
  // Увімкнути інтерактивність після монтування
  nextTick(() => {
    isInteractive.value = interactiveFeatures.value.manipulatable

    // Автоматично показати підказки для складних задач
    if (props.problemData.data?.level > 2) {
      showHints.value = true
    }
  })
})

// Спостерігачі
watch(
  () => props.problemData,
  (newData) => {
    // Скидати стан при зміні задачі
    userAnswer.value = null
    answerState.value = null
    showResult.value = false
    showCalculation.value = false
    showingSolution.value = false
  },
  { deep: true },
)

watch(showHints, (newValue) => {
  if (newValue) {
    // Автоматично показати підказку через кілька секунд
    setTimeout(() => {
      showHints.value = true
    }, 3000)
  }
})
</script>

<style scoped>
.interactive-geometry {
  max-width: 600px;
  margin: 0 auto;
  padding: 1.5rem;
  background: rgba(26, 16, 40, 0.6);
  border-radius: 16px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 215, 0, 0.2);
}

.geometry-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.challenge-title {
  font-family: 'Cinzel', serif;
  color: #ffd700;
  font-size: 1.25rem;
  margin: 0;
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
}

.shape-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: bold;
  background: rgba(123, 104, 238, 0.2);
  color: #7b68ee;
  border: 1px solid #7b68ee;
}

.shape-rectangle {
  background: rgba(74, 144, 226, 0.2);
  color: #4a90e2;
  border-color: #4a90e2;
}

.shape-circle {
  background: rgba(255, 107, 53, 0.2);
  color: #ff6b35;
  border-color: #ff6b35;
}

.shape-triangle {
  background: rgba(40, 167, 69, 0.2);
  color: #28a745;
  border-color: #28a745;
}

.visualization-container {
  background: rgba(10, 6, 18, 0.8);
  border-radius: 12px;
  padding: 1rem;
  margin-bottom: 1.5rem;
}

.geometry-canvas {
  width: 100%;
  max-width: 400px;
  height: auto;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.05);
  cursor: pointer;
  transition: all 0.3s ease;
}

.geometry-canvas:hover {
  border-color: rgba(255, 215, 0, 0.3);
}

.geometry-shape {
  fill: rgba(255, 215, 0, 0.3);
  stroke: #ffd700;
  stroke-width: 2;
  transition: all 0.3s ease;
}

.shape-group.interactive:hover .geometry-shape {
  fill: rgba(255, 215, 0, 0.5);
  stroke-width: 3;
}

.shape-group.highlighted .geometry-shape {
  fill: rgba(255, 215, 0, 0.6);
  filter: drop-shadow(0 0 5px #ffd700);
}

.geometry-shape.pulsing {
  animation: shapePulse 2s infinite ease-in-out;
}

@keyframes shapePulse {
  0%,
  100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.05);
  }
}

.dimension-line {
  stroke: #4a90e2;
  stroke-width: 1;
  marker-end: url(#arrowhead);
}

.dimension-text {
  fill: #4a90e2;
  font-family: 'Orbitron', monospace;
  font-size: 12px;
  font-weight: bold;
}

.radius-line {
  stroke-dasharray: 3, 3;
}

.hint-bubble {
  background: rgba(74, 144, 226, 0.9);
  border-radius: 8px;
  padding: 0.75rem;
  color: white;
  font-size: 0.85rem;
  animation: hintFadeIn 0.5s ease-out;
}

@keyframes hintFadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hint-formula {
  font-family: 'Orbitron', monospace;
  font-weight: bold;
  margin-top: 0.25rem;
  font-size: 0.9rem;
}

.geometry-tools {
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

.tool-group {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 1rem;
}

.tool-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #e8d5c7;
  font-size: 0.9rem;
  cursor: pointer;
}

.tool-checkbox {
  accent-color: #ffd700;
}

.calculation-display {
  padding: 1rem;
  background: rgba(74, 144, 226, 0.1);
  border-radius: 6px;
  border-left: 3px solid #4a90e2;
}

.formula-step,
.substitution-step,
.result-step {
  margin: 0.5rem 0;
  font-family: 'Orbitron', monospace;
}

.result-step {
  color: #ffd700;
  font-size: 1.1rem;
}

.answer-section {
  text-align: center;
  margin-bottom: 1.5rem;
}

.problem-statement {
  margin-bottom: 1rem;
  font-size: 1.1rem;
  line-height: 1.6;
}

.answer-input-group {
  display: flex;
  gap: 1rem;
  justify-content: center;
  align-items: center;
  margin-bottom: 1rem;
}

.geometry-answer-input {
  padding: 0.75rem;
  border: 2px solid rgba(123, 104, 238, 0.3);
  border-radius: 8px;
  background: rgba(10, 6, 18, 0.8);
  color: #e8d5c7;
  font-size: 1rem;
  width: 120px;
  text-align: center;
  transition: all 0.3s ease;
}

.geometry-answer-input:focus {
  outline: none;
  border-color: #ffd700;
  box-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
}

.geometry-answer-input.correct {
  border-color: #28a745;
  background: rgba(40, 167, 69, 0.1);
}

.geometry-answer-input.incorrect {
  border-color: #dc3545;
  background: rgba(220, 53, 69, 0.1);
  animation: inputShake 0.5s ease-out;
}

@keyframes inputShake {
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

.submit-geometry-button {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(145deg, #ffd700, #ff6b35);
  border: none;
  border-radius: 8px;
  color: #0a0612;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 120px;
}

.submit-geometry-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);
}

.submit-geometry-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.submit-geometry-button.calculating {
  background: linear-gradient(145deg, #6c757d, #495057);
  color: white;
}

.spinner {
  display: inline-block;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.show-solution-button {
  padding: 0.5rem 1rem;
  background: rgba(74, 144, 226, 0.2);
  border: 1px solid #4a90e2;
  border-radius: 6px;
  color: #4a90e2;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.show-solution-button:hover {
  background: rgba(74, 144, 226, 0.3);
  transform: translateY(-1px);
}

.step-by-step-solution {
  background: rgba(255, 215, 0, 0.1);
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: 12px;
  padding: 1.5rem;
  margin: 1rem 0;
}

.step-by-step-solution h4 {
  color: #ffd700;
  margin: 0 0 1rem 0;
  font-family: 'Cinzel', serif;
}

.solution-steps {
  margin: 1rem 0;
  padding-left: 1.5rem;
}

.solution-step {
  margin: 0.75rem 0;
  padding: 0.5rem;
  border-radius: 6px;
  transition: all 0.3s ease;
  font-family: 'Orbitron', monospace;
}

.solution-step.current {
  background: rgba(255, 215, 0, 0.2);
  border-left: 3px solid #ffd700;
  font-weight: bold;
  animation: stepHighlight 1.5s ease-in-out;
}

@keyframes stepHighlight {
  0%,
  100% {
    background: rgba(255, 215, 0, 0.2);
  }
  50% {
    background: rgba(255, 215, 0, 0.4);
  }
}

.close-solution-button {
  background: linear-gradient(145deg, #28a745, #20c997);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
}

.geometry-result {
  border-radius: 12px;
  padding: 1.5rem;
  margin-top: 1rem;
  text-align: center;
  animation: resultSlideIn 0.5s ease-out;
}

@keyframes resultSlideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.geometry-result.success {
  background: rgba(40, 167, 69, 0.1);
  border: 1px solid #28a745;
}

.geometry-result.error {
  background: rgba(220, 53, 69, 0.1);
  border: 1px solid #dc3545;
}

.result-header h4 {
  margin: 0 0 1rem 0;
  font-family: 'Cinzel', serif;
}

.success .result-header h4 {
  color: #28a745;
}
.error .result-header h4 {
  color: #dc3545;
}

.contextual-hint {
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(255, 193, 7, 0.1);
  border-left: 3px solid #ffc107;
  border-radius: 6px;
  text-align: left;
}

/* Адаптивність */
@media (max-width: 768px) {
  .interactive-geometry {
    padding: 1rem;
  }

  .geometry-header {
    flex-direction: column;
    text-align: center;
  }

  .answer-input-group {
    flex-direction: column;
    gap: 0.75rem;
  }

  .geometry-answer-input {
    width: 100%;
    max-width: 200px;
  }

  .tool-group {
    flex-direction: column;
    gap: 0.75rem;
  }
}
</style>
