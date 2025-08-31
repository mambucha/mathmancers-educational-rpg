<template>
  <div class="error-analysis-panel" v-if="showAnalysis">
    <div class="analysis-header">
      <h4 class="analysis-title">🔍 Аналіз помилки</h4>
      <button @click="$emit('close')" class="close-button">✕</button>
    </div>

    <!-- Основна діагностика -->
    <div class="primary-diagnosis" v-if="detailedHelp.primary_issue">
      <div class="diagnosis-badge" :class="severityClass">
        {{ getDiagnosisLabel(detailedHelp.primary_issue) }}
      </div>
      <div class="confidence-meter">
        <span>Впевненість: {{ Math.round(detailedHelp.confidence * 100) }}%</span>
        <div class="confidence-bar">
          <div
            class="confidence-fill"
            :style="{ width: detailedHelp.confidence * 100 + '%' }"
          ></div>
        </div>
      </div>
    </div>

    <!-- Пояснення помилки -->
    <div class="error-explanation">
      <h5>💡 Пояснення</h5>
      <p>{{ remediation }}</p>

      <!-- Аналогія для кращого розуміння -->
      <div v-if="detailedHelp.analogy" class="analogy-section">
        <h6>🎭 Уявіть собі:</h6>
        <p class="analogy-text">{{ detailedHelp.analogy }}</p>
      </div>
    </div>

    <!-- Візуальна демонстрація -->
    <div class="visual-demonstration" v-if="shouldShowVisualAid">
      <h5>👁️ Візуальна допомога</h5>

      <!-- Демонстрація балансу для помилок рівноваги -->
      <div v-if="detailedHelp.visual_aid === 'balance_scale_animation'" class="balance-demo">
        <div class="demo-title">Неправильно:</div>
        <div class="broken-balance">
          <div class="balance-left unbalanced">2x + 3</div>
          <div class="balance-center">≠</div>
          <div class="balance-right">7 - 3</div>
        </div>
        <div class="demo-title correct">Правильно:</div>
        <div class="correct-balance">
          <div class="balance-left balanced">2x + 3 - 3</div>
          <div class="balance-center">=</div>
          <div class="balance-right balanced">7 - 3</div>
        </div>
      </div>

      <!-- Демонстрація обернених операцій -->
      <div v-else-if="detailedHelp.visual_aid === 'inverse_operations_chart'" class="inverse-demo">
        <div class="operation-pairs">
          <div class="pair">
            <span class="operation">+ 5</span>
            <span class="arrow">⟷</span>
            <span class="inverse">- 5</span>
          </div>
          <div class="pair">
            <span class="operation">× 3</span>
            <span class="arrow">⟷</span>
            <span class="inverse">÷ 3</span>
          </div>
        </div>
        <div class="demo-explanation">Кожна операція має свою "протилежність" для скасування</div>
      </div>

      <!-- Кольорове кодування знаків -->
      <div v-else-if="detailedHelp.visual_aid === 'sign_tracking_colors'" class="sign-demo">
        <div class="equation-with-colors">
          <span class="term">x</span>
          <span class="sign positive">+</span>
          <span class="term">5</span>
          <span class="equals">=</span>
          <span class="term">8</span>
        </div>
        <div class="sign-rule">
          <span class="rule-text">Щоб прибрати </span>
          <span class="sign positive">+5</span>
          <span class="rule-text">, робимо </span>
          <span class="sign negative">-5</span>
        </div>
      </div>
    </div>

    <!-- Практичні поради -->
    <div class="practice-tips" v-if="detailedHelp.practice_tip">
      <h5>🎯 Порада для практики</h5>
      <p>{{ detailedHelp.practice_tip }}</p>
    </div>

    <!-- Індикатор частоти помилки -->
    <div class="frequency-indicator" v-if="errorAnalysis.frequency > 1">
      <div class="frequency-warning" :class="frequencyClass">
        <span class="warning-icon">⚠️</span>
        <span>Ця помилка повторюється ({{ errorAnalysis.frequency }} разів)</span>
      </div>
      <div class="frequency-advice">
        <p>Рекомендую зосередитись на цій концепції перед переходом далі.</p>
      </div>
    </div>

    <!-- Кнопки дій -->
    <div class="action-buttons">
      <button @click="$emit('show-hint')" class="hint-button">💡 Показати підказку</button>
      <button
        @click="$emit('try-simpler')"
        class="simpler-button"
        v-if="detailedHelp.severity > 0.7"
      >
        📚 Спростити задачу
      </button>
      <button @click="$emit('close')" class="continue-button">✅ Зрозумів, спробую ще раз</button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  showAnalysis: {
    type: Boolean,
    default: false,
  },
  errorAnalysis: {
    type: Object,
    required: true,
  },
  remediation: {
    type: String,
    required: true,
  },
  detailedHelp: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['close', 'show-hint', 'try-simpler'])

// Обчислювані властивості
const severityClass = computed(() => {
  const severity = props.detailedHelp.severity || 0
  if (severity > 0.8) return 'severe'
  if (severity > 0.5) return 'moderate'
  return 'mild'
})

const frequencyClass = computed(() => {
  const frequency = props.errorAnalysis.frequency || 0
  if (frequency > 4) return 'high-frequency'
  if (frequency > 2) return 'medium-frequency'
  return 'low-frequency'
})

const shouldShowVisualAid = computed(() => {
  return props.detailedHelp.visual_aid && props.detailedHelp.visual_aid !== 'step_by_step_guide'
})

// Методи
const getDiagnosisLabel = (issue) => {
  const labels = {
    equation_statement: 'Рівняння як приклад',
    operation_reversal: 'Плутання операцій',
    balance_violation: 'Порушення рівноваги',
    sign_error: 'Помилка із знаками',
    coefficient_confusion: 'Плутання коефіцієнтів',
  }
  return labels[issue] || 'Математична помилка'
}
</script>

<style scoped>
.error-analysis-panel {
  background: linear-gradient(135deg, rgba(220, 20, 60, 0.1), rgba(255, 99, 71, 0.05));
  border: 2px solid rgba(220, 20, 60, 0.3);
  border-radius: 16px;
  padding: 1.5rem;
  margin: 1rem 0;
  backdrop-filter: blur(10px);
  position: relative;
}

.analysis-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.analysis-title {
  color: #dc143c;
  font-family: 'Cinzel', serif;
  margin: 0;
  text-shadow: 0 0 10px rgba(220, 20, 60, 0.3);
}

.close-button {
  background: none;
  border: none;
  color: #dc143c;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.close-button:hover {
  background: rgba(220, 20, 60, 0.1);
  transform: rotate(90deg);
}

/* Діагностика */
.primary-diagnosis {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.diagnosis-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: bold;
  font-size: 0.9rem;
}

.diagnosis-badge.severe {
  background: rgba(220, 20, 60, 0.2);
  color: #dc143c;
  border: 1px solid #dc143c;
}

.diagnosis-badge.moderate {
  background: rgba(255, 193, 7, 0.2);
  color: #ffc107;
  border: 1px solid #ffc107;
}

.diagnosis-badge.mild {
  background: rgba(40, 167, 69, 0.2);
  color: #28a745;
  border: 1px solid #28a745;
}

.confidence-meter {
  flex: 1;
  min-width: 150px;
}

.confidence-meter span {
  font-size: 0.8rem;
  color: #e8d5c7;
  display: block;
  margin-bottom: 0.25rem;
}

.confidence-bar {
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  overflow: hidden;
}

.confidence-fill {
  height: 100%;
  background: linear-gradient(90deg, #dc143c, #ff6b35);
  border-radius: 4px;
  transition: width 0.5s ease;
}

/* Пояснення */
.error-explanation {
  background: rgba(10, 6, 18, 0.6);
  border-radius: 12px;
  padding: 1.25rem;
  margin-bottom: 1rem;
}

.error-explanation h5 {
  color: #ffd700;
  margin: 0 0 0.75rem 0;
  font-family: 'Cinzel', serif;
}

.analogy-section {
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(74, 144, 226, 0.1);
  border-left: 3px solid #4a90e2;
  border-radius: 8px;
}

.analogy-section h6 {
  color: #4a90e2;
  margin: 0 0 0.5rem 0;
}

.analogy-text {
  font-style: italic;
  color: #e8d5c7;
  margin: 0;
}

/* Візуальні демонстрації */
.visual-demonstration {
  background: rgba(123, 104, 238, 0.1);
  border-radius: 12px;
  padding: 1.25rem;
  margin-bottom: 1rem;
}

.visual-demonstration h5 {
  color: #7b68ee;
  margin: 0 0 1rem 0;
  font-family: 'Cinzel', serif;
}

/* Демонстрація балансу */
.balance-demo {
  text-align: center;
}

.demo-title {
  font-weight: bold;
  margin: 0.5rem 0;
  color: #dc143c;
}

.demo-title.correct {
  color: #28a745;
}

.broken-balance,
.correct-balance {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin: 1rem 0;
  font-family: 'Orbitron', monospace;
  font-size: 1.1rem;
}

.balance-left.unbalanced,
.balance-right.unbalanced {
  color: #dc143c;
  text-decoration: line-through;
}

.balance-left.balanced,
.balance-right.balanced {
  color: #28a745;
}

.balance-center {
  font-weight: bold;
  font-size: 1.3rem;
}

/* Демонстрація обернених операцій */
.operation-pairs {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
}

.pair {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-family: 'Orbitron', monospace;
  font-size: 1.2rem;
}

.operation,
.inverse {
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  min-width: 60px;
  text-align: center;
}

.arrow {
  color: #ffd700;
  font-weight: bold;
}

.demo-explanation {
  text-align: center;
  margin-top: 1rem;
  font-style: italic;
  color: #e8d5c7;
}

/* Кольорові знаки */
.equation-with-colors {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  font-family: 'Orbitron', monospace;
  font-size: 1.3rem;
  margin-bottom: 1rem;
}

.term {
  color: #e8d5c7;
}

.sign.positive {
  color: #28a745;
  font-weight: bold;
}

.sign.negative {
  color: #dc143c;
  font-weight: bold;
}

.equals {
  color: #ffd700;
  font-weight: bold;
}

.sign-rule {
  text-align: center;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

.rule-text {
  color: #e8d5c7;
}

/* Практичні поради */
.practice-tips {
  background: rgba(255, 215, 0, 0.1);
  border-radius: 12px;
  padding: 1.25rem;
  margin-bottom: 1rem;
}

.practice-tips h5 {
  color: #ffd700;
  margin: 0 0 0.75rem 0;
  font-family: 'Cinzel', serif;
}

/* Індикатор частоти */
.frequency-indicator {
  margin-bottom: 1rem;
}

.frequency-warning {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  border-radius: 8px;
  margin-bottom: 0.5rem;
}

.frequency-warning.high-frequency {
  background: rgba(220, 20, 60, 0.2);
  border: 1px solid #dc143c;
  color: #dc143c;
}

.frequency-warning.medium-frequency {
  background: rgba(255, 193, 7, 0.2);
  border: 1px solid #ffc107;
  color: #ffc107;
}

.frequency-advice {
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  font-size: 0.9rem;
}

/* Кнопки дій */
.action-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
}

.hint-button,
.simpler-button,
.continue-button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-family: 'Cinzel', serif;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.hint-button {
  background: linear-gradient(145deg, #4a90e2, #7b68ee);
  color: white;
}

.simpler-button {
  background: linear-gradient(145deg, #ffc107, #ff6b35);
  color: #0a0612;
}

.continue-button {
  background: linear-gradient(145deg, #28a745, #20c997);
  color: white;
}

.hint-button:hover,
.simpler-button:hover,
.continue-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

/* Адаптивність */
@media (max-width: 768px) {
  .error-analysis-panel {
    padding: 1rem;
  }

  .primary-diagnosis {
    flex-direction: column;
    align-items: stretch;
  }

  .action-buttons {
    flex-direction: column;
  }

  .pair {
    font-size: 1rem;
  }

  .equation-with-colors {
    font-size: 1.1rem;
  }
}
</style>
