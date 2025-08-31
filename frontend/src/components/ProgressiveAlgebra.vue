.remediation-advice { background: rgba(255, 193, 7, 0.1); border-left: 4px solid #ffc107; padding:
1rem; margin: 1rem 0; } .analysis-button { display: block; margin: 1rem auto 0; padding: 0.5rem
1rem; background: linear-gradient(145deg, #dc143c, #ff6b35); color: white; border: none;
border-radius: 6px; cursor: pointer; font-size: 0.9rem; transition: all 0.3s ease; }
.analysis-button:hover { transform: translateY(-2px);
<template>
  <div class="progressive-algebra-container">
    <!-- Заголовок з індикатором прогресу -->
    <div class="algebra-header">
      <h3 class="step-title">{{ currentStep.title }}</h3>
      <div class="progress-indicator">
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
        </div>
        <span class="step-counter">Крок {{ currentStepIndex + 1 }} з {{ totalSteps }}</span>
      </div>
    </div>

    <!-- Концептуальне введення -->
    <div v-if="currentStep.step_type === 'concept_intro'" class="concept-intro">
      <div class="magical-balance">
        <div class="balance-scale">
          <div class="balance-arm"></div>
          <div class="balance-left-pan">
            <div class="equation-side">{{ currentStep.equation_display.left }}</div>
          </div>
          <div class="balance-right-pan">
            <div class="equation-side">{{ currentStep.equation_display.right }}</div>
          </div>
          <div class="balance-fulcrum"></div>
        </div>
        <div class="balance-status" :class="currentStep.equation_display.balance_state">
          ⚖️ Ваги у рівновазі
        </div>
      </div>

      <div class="narration-box">
        <p class="narration-text">{{ currentStep.narration }}</p>
        <div class="concept-explanation">
          <strong>Концепція:</strong> {{ currentStep.concept_explanation }}
        </div>
        <div v-if="currentStep.visual_hint" class="visual-hint">
          💡 {{ currentStep.visual_hint }}
        </div>
      </div>

      <button @click="proceedToNext" class="proceed-button">Зрозуміло, продовжуємо</button>
    </div>

    <!-- Планування стратегії -->
    <div v-else-if="currentStep.step_type === 'planning'" class="planning-step">
      <div class="current-equation-display">
        <span class="equation-left">{{ currentStep.current_equation.left }}</span>
        <span class="equation-equals"> = </span>
        <span class="equation-right">{{ currentStep.current_equation.right }}</span>
      </div>

      <div class="planning-content">
        <div class="goal-statement">
          <h4>🎯 Мета:</h4>
          <p>{{ currentStep.goal }}</p>
        </div>

        <div class="strategic-question">
          <h4>🤔 Питання для роздумів:</h4>
          <p>{{ currentStep.question }}</p>
        </div>

        <div class="insight-revelation">
          <h4>💡 Розуміння:</h4>
          <p>{{ currentStep.correct_insight }}</p>
          <p class="planning-hint"><strong>Підказка:</strong> {{ currentStep.planning_hint }}</p>
        </div>

        <div v-if="showGuidance" class="stage-guidance">
          {{ currentStep.stage_guidance.guidance }}
        </div>
      </div>

      <button @click="proceedToNext" class="proceed-button">Готовий до дії!</button>
    </div>

    <!-- Виконання операції -->
    <div
      v-else-if="
        currentStep.step_type === 'execute_operation' || currentStep.step_type === 'final_isolation'
      "
      class="operation-step"
    >
      <div class="operation-question">
        <h4>{{ currentStep.title }}</h4>
        <p>{{ currentStep.question }}</p>
      </div>

      <!-- Візуальна трансформація (якщо доступна) -->
      <div v-if="currentStep.visual_transformation" class="visual-transformation">
        <div class="transformation-before">
          <h5>До операції:</h5>
          <div class="equation-display">
            <span>{{ currentStep.visual_transformation.before.left }}</span>
            <span> = </span>
            <span>{{ currentStep.visual_transformation.before.right }}</span>
          </div>
        </div>

        <div class="transformation-arrow">
          <span class="operation-symbol">{{ currentStep.visual_transformation.operation }}</span>
          <span class="arrow">↓</span>
        </div>

        <div class="transformation-after" v-if="selectedOperation">
          <h5>Після операції:</h5>
          <div class="equation-display">
            <span>{{ currentStep.visual_transformation.after.left }}</span>
            <span> = </span>
            <span>{{ currentStep.visual_transformation.after.right }}</span>
          </div>
        </div>
      </div>

      <!-- Варіанти операцій -->
      <div class="operation-options">
        <button
          v-for="option in currentStep.options"
          :key="option.operation"
          @click="selectOperation(option)"
          class="operation-option"
          :class="{
            selected: selectedOperation === option.operation,
            correct: showResults && option.correct,
            incorrect: showResults && !option.correct && selectedOperation === option.operation,
          }"
          :disabled="showResults"
        >
          {{ option.description }}
        </button>
      </div>

      <!-- Керівництво залежно від рівня -->
      <div v-if="showGuidance && currentStep.stage_guidance.guidance" class="stage-guidance">
        {{ currentStep.stage_guidance.guidance }}
      </div>

      <!-- Результат вибору -->
      <div v-if="showResults" class="operation-result">
        <div
          class="result-explanation"
          :class="{ correct: lastResult.is_correct, incorrect: !lastResult.is_correct }"
        >
          <h5 v-if="lastResult.is_correct">✅ Правильно!</h5>
          <h5 v-else>❌ Неправильно</h5>
          <p>{{ lastResult.feedback }}</p>
        </div>

        <div v-if="currentStep.explanation" class="detailed-explanation">
          <strong>Пояснення:</strong> {{ currentStep.explanation }}
        </div>

        <div v-if="currentStep.celebration" class="celebration">
          🎉 {{ currentStep.celebration }}
        </div>

        <!-- Додаткові поради при помилці -->
        <div v-if="!lastResult.is_correct && lastResult.remediation" class="remediation-advice">
          <h5>📚 Порада:</h5>
          <p>{{ lastResult.remediation }}</p>
        </div>

        <div v-if="!lastResult.is_correct && lastResult.encouragement" class="encouragement">
          <p>
            <em>{{ lastResult.encouragement }}</em>
          </p>
        </div>

        <!-- Кнопки для продовження -->
        <div class="action-buttons">
          <button
            v-if="lastResult.is_correct && !lastResult.is_equation_solved"
            @click="proceedToNext"
            class="proceed-button"
          >
            Наступний крок
          </button>
          <button
            v-else-if="lastResult.is_correct && lastResult.is_equation_solved"
            @click="$emit('equation-completed')"
            class="complete-button"
          >
            Завершити рівняння
          </button>
          <button v-else @click="tryAgain" class="retry-button">Спробувати ще раз</button>
        </div>
      </div>
    </div>

    <!-- Індикатор майстерності -->
    <div class="mastery-indicator" v-if="masteryData">
      <h5>📈 Ваш прогрес:</h5>
      <div class="mastery-bars">
        <div class="mastery-item">
          <span>Розуміння рівноваги:</span>
          <div class="mastery-bar">
            <div
              class="mastery-fill"
              :style="{ width: masteryData.balance_mastery * 100 + '%' }"
            ></div>
          </div>
        </div>
        <div class="mastery-item">
          <span>Обернені операції:</span>
          <div class="mastery-bar">
            <div
              class="mastery-fill"
              :style="{ width: masteryData.operations_mastery * 100 + '%' }"
            ></div>
          </div>
        </div>
        <div class="mastery-item">
          <span>Розв'язування рівнянь:</span>
          <div class="mastery-bar">
            <div
              class="mastery-fill"
              :style="{ width: masteryData.equation_mastery * 100 + '%' }"
            ></div>
          </div>
        </div>
      </div>
      <div v-if="masteryData.streak > 2" class="streak-indicator">
        🔥 Серія: {{ masteryData.streak }} правильних відповідей!
      </div>
    </div>

    <!-- Компонент поглибленого аналізу помилок -->
    <ErrorAnalysisPanel
      v-if="lastResult && lastResult.detailed_help"
      :show-analysis="showErrorAnalysis"
      :error-analysis="lastResult.error_analysis || {}"
      :remediation="lastResult.remediation || ''"
      :detailed-help="lastResult.detailed_help || {}"
      @close="handleCloseErrorAnalysis"
      @show-hint="handleShowHint"
      @try-simpler="handleTrySimpler"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import ErrorAnalysisPanel from './ErrorAnalysisPanel.vue'

const props = defineProps({
  problemData: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['operation-selected', 'equation-completed', 'next-step'])

// Реактивні дані
const selectedOperation = ref('')
const showResults = ref(false)
const lastResult = ref(null)
const showErrorAnalysis = ref(false)

// Обчислювані властивості
const balanceSteps = computed(() => props.problemData.balance_steps || [])
const currentStepIndex = computed(() => props.problemData.current_step || 0)
const currentStep = computed(() => balanceSteps.value[currentStepIndex.value] || {})
const totalSteps = computed(() => balanceSteps.value.length)
const progressPercentage = computed(() => ((currentStepIndex.value + 1) / totalSteps.value) * 100)

const showGuidance = computed(() => {
  const adaptiveFeatures = props.problemData.adaptive_features || {}
  return adaptiveFeatures.provide_hints && currentStep.value.stage_guidance?.guidance
})

const masteryData = computed(() => props.problemData.player_mastery || null)

// Методи для обробки аналізу помилок
const handleShowErrorAnalysis = () => {
  showErrorAnalysis.value = true
}

const handleCloseErrorAnalysis = () => {
  showErrorAnalysis.value = false
}

const handleShowHint = () => {
  // Логіка показу додаткової підказки
  showErrorAnalysis.value = false
}

const handleTrySimpler = () => {
  // Сигнал батьківському компоненту спростити задачу
  emit('try-simpler-problem')
  showErrorAnalysis.value = false
}

// Методи
const selectOperation = (option) => {
  if (showResults.value) return

  selectedOperation.value = option.operation
  emit('operation-selected', option.operation)
}

const proceedToNext = () => {
  emit('next-step')
}

const tryAgain = () => {
  selectedOperation.value = ''
  showResults.value = false
  lastResult.value = null
  showErrorAnalysis.value = false
}

// Слухач для результатів від батьківського компонента
const showOperationResult = (result) => {
  lastResult.value = result
  showResults.value = true

  // Показуємо поглиблений аналіз для неправильних відповідей
  if (!result.is_correct && result.detailed_help) {
    setTimeout(() => {
      showErrorAnalysis.value = true
    }, 1000) // Невелика затримка для кращого UX
  }
}

// Скидання стану при зміні кроку
watch(
  () => currentStepIndex.value,
  () => {
    selectedOperation.value = ''
    showResults.value = false
    lastResult.value = null
  },
)

// Експортуємо метод для батьківського компонента
defineExpose({
  showOperationResult,
})
</script>

<style scoped>
.progressive-algebra-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 1.5rem;
  font-family: 'Crimson Text', serif;
}

.algebra-header {
  text-align: center;
  margin-bottom: 2rem;
}

.step-title {
  font-family: 'Cinzel', serif;
  color: #ffd700;
  font-size: 1.5rem;
  margin-bottom: 1rem;
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
}

.progress-indicator {
  display: flex;
  align-items: center;
  gap: 1rem;
  justify-content: center;
}

.progress-bar {
  width: 200px;
  height: 8px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #4a90e2, #7b68ee);
  transition: width 0.3s ease;
}

.step-counter {
  font-size: 0.9rem;
  color: #e8d5c7;
  opacity: 0.8;
}

/* Магічні ваги */
.magical-balance {
  text-align: center;
  margin: 2rem 0;
}

.balance-scale {
  position: relative;
  width: 300px;
  height: 150px;
  margin: 0 auto;
}

.balance-arm {
  position: absolute;
  top: 40px;
  left: 50px;
  width: 200px;
  height: 4px;
  background: #8b5a96;
  border-radius: 2px;
}

.balance-left-pan,
.balance-right-pan {
  position: absolute;
  top: 60px;
  width: 80px;
  height: 60px;
  background: linear-gradient(135deg, #7b68ee, #4a90e2);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.balance-left-pan {
  left: 40px;
}

.balance-right-pan {
  right: 40px;
}

.equation-side {
  font-family: 'Orbitron', monospace;
  font-weight: bold;
  color: white;
  font-size: 0.9rem;
}

.balance-fulcrum {
  position: absolute;
  top: 44px;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 15px solid transparent;
  border-right: 15px solid transparent;
  border-bottom: 20px solid #8b5a96;
}

.balance-status {
  margin-top: 1rem;
  font-size: 1.1rem;
  color: #28a745;
}

/* Блоки з текстом */
.narration-box,
.planning-content,
.operation-result {
  background: rgba(26, 16, 40, 0.6);
  border: 1px solid rgba(255, 215, 0, 0.2);
  border-radius: 12px;
  padding: 1.5rem;
  margin: 1.5rem 0;
  backdrop-filter: blur(10px);
}

.narration-text {
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.concept-explanation {
  background: rgba(74, 144, 226, 0.1);
  border-left: 3px solid #4a90e2;
  padding: 1rem;
  margin: 1rem 0;
  font-style: italic;
}

.visual-hint {
  background: rgba(255, 215, 0, 0.1);
  border-left: 3px solid #ffd700;
  padding: 1rem;
  margin: 1rem 0;
  color: #ffd700;
}

/* Відображення рівнянь */
.current-equation-display,
.equation-display {
  font-family: 'Orbitron', monospace;
  font-size: 2rem;
  text-align: center;
  margin: 1.5rem 0;
  color: #e8d5c7;
}

/* Варіанти операцій */
.operation-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
  margin: 1.5rem 0;
}

.operation-option {
  padding: 1rem 1.5rem;
  background: rgba(10, 6, 18, 0.8);
  border: 2px solid rgba(123, 104, 238, 0.3);
  border-radius: 8px;
  color: #e8d5c7;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.95rem;
  text-align: center;
}

.operation-option:hover:not(:disabled) {
  border-color: #ffd700;
  background: rgba(10, 6, 18, 0.9);
  transform: translateY(-2px);
}

.operation-option.selected {
  border-color: #4a90e2;
  background: rgba(74, 144, 226, 0.2);
}

.operation-option.correct {
  border-color: #28a745;
  background: rgba(40, 167, 69, 0.2);
  color: #28a745;
}

.operation-option.incorrect {
  border-color: #dc3545;
  background: rgba(220, 53, 69, 0.2);
  color: #dc3545;
}

/* Результати */
.result-explanation.correct {
  border-left: 4px solid #28a745;
  background: rgba(40, 167, 69, 0.1);
}

.result-explanation.incorrect {
  border-left: 4px solid #dc3545;
  background: rgba(220, 53, 69, 0.1);
}

.detailed-explanation {
  margin: 1rem 0;
  padding: 1rem;
  background: rgba(74, 144, 226, 0.1);
  border-radius: 6px;
}

.celebration {
  text-align: center;
  font-size: 1.2rem;
  color: #ffd700;
  margin: 1rem 0;
}

.remediation-advice {
  background: rgba(255, 193, 7, 0.1);
  border-left: 4px solid #ffc107;
  padding: 1rem;
  margin: 1rem 0;
}

.encouragement {
  text-align: center;
  font-style: italic;
  color: #7b68ee;
  margin: 1rem 0;
}

/* Кнопки */
.proceed-button,
.complete-button,
.retry-button {
  display: block;
  margin: 1.5rem auto;
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 8px;
  font-family: 'Cinzel', serif;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.proceed-button,
.complete-button {
  background: linear-gradient(145deg, #ffd700, #ff6b35);
  color: #0a0612;
}

.retry-button {
  background: linear-gradient(145deg, #6c757d, #495057);
  color: white;
}

.proceed-button:hover,
.complete-button:hover,
.retry-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

/* Індикатор майстерності */
.mastery-indicator {
  background: rgba(26, 16, 40, 0.6);
  border: 1px solid rgba(123, 104, 238, 0.3);
  border-radius: 12px;
  padding: 1.5rem;
  margin-top: 2rem;
}

.mastery-bars {
  margin: 1rem 0;
}

.mastery-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 0.8rem 0;
}

.mastery-item span {
  min-width: 140px;
  font-size: 0.9rem;
}

.mastery-bar {
  flex: 1;
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  overflow: hidden;
}

.mastery-fill {
  height: 100%;
  background: linear-gradient(90deg, #ff6b35, #ffd700);
  transition: width 0.5s ease;
}

.streak-indicator {
  text-align: center;
  margin-top: 1rem;
  font-weight: bold;
  color: #ff6b35;
}

/* Адаптивність */
@media (max-width: 768px) {
  .progressive-algebra-container {
    padding: 1rem;
  }

  .balance-scale {
    width: 250px;
    height: 120px;
  }

  .current-equation-display,
  .equation-display {
    font-size: 1.5rem;
  }

  .operation-options {
    grid-template-columns: 1fr;
  }

  .progress-indicator {
    flex-direction: column;
    gap: 0.5rem;
  }

  .progress-bar {
    width: 150px;
  }
}
</style>
