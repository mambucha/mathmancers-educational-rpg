<script setup>
import RegistrationForm from '@/components/RegistrationForm.vue'
import LoginForm from '@/components/LoginForm.vue'
</script>

<template>
  <div class="mathmancers-home">
    <!-- Космічні математичні рівняння у фоні -->
    <div class="cosmic-equations">
      <div
        v-for="(equation, i) in cosmicEquations"
        :key="`equation-${i}`"
        class="floating-equation"
        :style="{
          '--delay': Math.random() * 20 + 's',
          '--duration': Math.random() * 15 + 25 + 's',
          '--color': equationColors[i % equationColors.length],
          left: Math.random() * 100 + '%',
        }"
      >
        {{ equation }}
      </div>
    </div>

    <!-- Астральні руни що обертаються -->
    <div class="astral-runes">
      <div
        v-for="(rune, i) in astralRunes"
        :key="`rune-${i}`"
        class="cosmic-rune"
        :style="{
          '--delay': i * 3 + 's',
          '--duration': Math.random() * 10 + 25 + 's',
          '--color': runeColors[i % runeColors.length],
          left: Math.random() * 90 + '%',
          top: Math.random() * 80 + '%',
        }"
      >
        {{ rune }}
      </div>
    </div>

    <!-- Головний логотип та заголовок гри -->
    <header class="game-logo">
      <h1 class="game-title">MathMancers</h1>
      <p class="game-subtitle">The Last Arithmancer</p>
      <p class="game-tagline">Transform Fear into Power through Mathematics</p>

      <!-- Індикатор Хаосу Обчислень -->
      <div class="chaos-warning"></div>
    </header>

    <!-- Область авторизації -->
    <main class="auth-realm">
      <!-- Панель реєстрації - Нові Учні -->
      <section class="spell-panel registration-panel">
        <div class="panel-icon">🔮</div>
        <h2 class="panel-title">Join the Academy</h2>
        <RegistrationForm />
        <div class="soul-scribe-glow"></div>
      </section>

      <!-- Панель входу - Повернення Арифмансера -->
      <section class="spell-panel login-panel">
        <div class="panel-icon">🧙‍♂️</div>
        <h2 class="panel-title">Return to the Sanctum</h2>
        <LoginForm />
        <div class="soul-scribe-glow"></div>
      </section>
    </main>

    <!-- Додатковий магічний елемент - цитата дідуся Еліана -->
    <footer class="elian-wisdom">
      <p class="wisdom-quote">
        "Mathematics is not numbers and equations... it's the language of the cosmos itself."
      </p>
      <p class="wisdom-author">— Grandfather Elian, Last Grand Arithmancer</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  data() {
    return {
      // Космічні математичні рівняння для анімації
      cosmicEquations: [
        'E = mc²',
        '∫ f(x) dx',
        '∑ n=1∞',
        'lim x→∞',
        'π r²',
        '√(a² + b²)',
        'f(x) = ax + b',
        'sin²θ + cos²θ = 1',
        '∇²ψ = 0',
        'Δx Δp ≥ ℏ/2',
        'e^(iπ) + 1 = 0',
        '∂f/∂x',
        'log₂(x)',
        '|z|² = z·z*',
        'det(A)',
      ],

      // Кольори для рівнянь
      equationColors: [
        '#ffd700', // Золото
        '#4a90e2', // Магічний синій
        '#7b68ee', // Спадкова магія
        '#00ffff', // Кристалічний ціан
        '#ff6b35', // Енергійний помаранчевий
      ],

      // Астральні руни та символи
      astralRunes: [
        '∞',
        '∑',
        '∫',
        '∂',
        '∇',
        'π',
        'φ',
        'θ',
        'λ',
        'μ',
        'α',
        'β',
        'γ',
        'δ',
        'ε',
        '∀',
        '∃',
        '∈',
        '⊆',
        '∪',
      ],

      // Кольори для рун
      runeColors: [
        '#7b68ee', // Спадкова магія
        '#4a90e2', // Магічний синій
        '#ffd700', // Золото
        '#ff6b35', // Енергійний помаранчевий
      ],
    }
  },
}
</script>

<style scoped>
/* Додаткові стилі для цитати дідуся Еліана */
.elian-wisdom {
  position: absolute;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
  max-width: 600px;
  z-index: 5;
  opacity: 0.8;
}

.wisdom-quote {
  font-family: 'Crimson Text', serif;
  font-size: clamp(0.875rem, 2vw, 1.125rem);
  font-style: italic;
  color: #7b68ee;
  margin-bottom: 0.5rem;
  text-shadow: 0 0 10px rgba(123, 104, 238, 0.3);
}

.wisdom-author {
  font-family: 'Cinzel', serif;
  font-size: clamp(0.75rem, 1.5vw, 0.875rem);
  color: #ffd700;
  opacity: 0.9;
  text-shadow: 0 0 8px rgba(255, 215, 0, 0.4);
}

/* Адаптивність для мобільних */
@media (max-width: 768px) {
  .elian-wisdom {
    bottom: 1rem;
    left: 1rem;
    right: 1rem;
    transform: none;
    max-width: none;
  }

  .wisdom-quote {
    font-size: 0.875rem;
  }

  .wisdom-author {
    font-size: 0.75rem;
  }
}

/* Спеціальні анімації для HomeView */
@keyframes homePageEntry {
  0% {
    opacity: 0;
    transform: translateY(50px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.mathmancers-home {
  animation: homePageEntry 1s ease-out;
}

.game-logo {
  animation: homePageEntry 1.2s ease-out;
}

.auth-realm {
  animation: homePageEntry 1.4s ease-out;
}

.elian-wisdom {
  animation: homePageEntry 1.6s ease-out;
}
</style>
