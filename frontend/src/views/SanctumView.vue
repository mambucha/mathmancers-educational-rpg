<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import api from '@/services/api'

const playerStats = ref(null)
const isLoading = ref(true)

onMounted(async () => {
  try {
    // --- СПОЧАТКУ ЗЦІЛЮЄМО ГРАВЦЯ ---
    await api.healPlayer()

    // --- ПОТІМ ЗАВАНТАЖУЄМО ЙОГО ОНОВЛЕНІ ДАНІ ---
    const response = await api.getPlayerStats()
    playerStats.value = response.data
  } catch (error) {
    console.error('Не вдалося завантажити дані гравця:', error)
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <div class="sanctum-container">
    <!-- Містичні частинки у фоні (зменшено кількість) -->
    <div class="mystical-particles">
      <div
        v-for="i in 20"
        :key="`particle-${i}`"
        class="mystical-particle"
        :style="{
          '--delay': Math.random() * 15 + 's',
          '--duration': Math.random() * 10 + 20 + 's',
          '--size': Math.random() * 3 + 2 + 'px',
          '--color': ['#d4af37', '#8b5a96', '#4a6fa5'][Math.floor(Math.random() * 3)],
        }"
      ></div>
    </div>

    <!-- Плаваючі магічні руни (зменшено кількість) -->
    <div class="floating-runes">
      <div
        v-for="(rune, i) in ['∫', '∑', '∞', 'π', '√', 'Δ']"
        :key="`rune-${i}`"
        class="floating-rune"
        :style="{
          '--delay': i * 2.5 + 's',
          '--color': ['#d4af37', '#8b5a96'][i % 2],
          left: Math.random() * 90 + '%',
          top: Math.random() * 70 + '%',
        }"
      >
        {{ rune }}
      </div>
    </div>

    <div class="sanctum-content-wrapper">
      <!-- Стан завантаження -->
      <div v-if="isLoading" class="sanctum-loading">
        <div class="loading-constellation">
          <div v-for="i in 6" :key="`star-${i}`" class="constellation-star"></div>
        </div>
        <div class="loading-inscription">Відновлення зв'язку зі Спадщиною...</div>
      </div>

      <!-- Основний контент Святилища -->
      <div v-else-if="playerStats" class="sanctum-main">
        <!-- Заголовок Святилища (компактніший) -->
        <div class="text-center mb-6">
          <h1 class="sanctum-title">Святилище Арифмансера</h1>
          <div class="sanctum-subtitle">Тут живе спадщина дідуся Еліана</div>
        </div>

        <!-- Привітання з аватаром (компактніше) -->
        <div class="sanctum-welcome">
          <div class="heritage-avatar">
            <div class="avatar-orb">🧙‍♂️</div>
            <div class="avatar-ring"></div>
          </div>
          <div class="text-center">
            <p class="text-base text-sanctum-light mb-1">Вітаємо, спадкоємче</p>
            <div class="heritage-name">{{ playerStats.owner.username }}</div>
          </div>
        </div>

        <!-- Панель Мудрості та Характеристик (компактніша) -->
        <div class="wisdom-panel">
          <div class="wisdom-header">
            <h3 class="wisdom-title">Сила Спадщини</h3>
            <div class="ancient-divider"></div>
          </div>

          <div class="wisdom-grid">
            <!-- Кристал Рівня -->
            <div class="stat-crystal level-crystal">
              <div class="stat-icon-container">
                <div class="stat-mystical-icon">⭐</div>
                <div>
                  <div class="stat-label">Рівень Мудрості</div>
                  <div class="stat-value">{{ playerStats.level }}</div>
                </div>
              </div>
            </div>

            <!-- Кристал Досвіду -->
            <div class="stat-crystal experience-crystal">
              <div class="stat-icon-container">
                <div class="stat-mystical-icon">📜</div>
                <div class="flex-1">
                  <div class="stat-label">Зібрана Мудрість</div>
                  <div class="stat-value">{{ playerStats.xp }}/{{ 100 * playerStats.level }}</div>
                  <div class="essence-bar">
                    <div
                      class="essence-fill"
                      :style="{ width: (playerStats.xp / (100 * playerStats.level)) * 100 + '%' }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Кристал Здоров'я -->
            <div class="stat-crystal health-crystal">
              <div class="stat-icon-container">
                <div class="stat-mystical-icon">💚</div>
                <div class="flex-1">
                  <div class="stat-label">Життєва Сила</div>
                  <div class="stat-value">{{ playerStats.hp }}/{{ playerStats.max_hp }}</div>
                  <div class="essence-bar">
                    <div
                      class="essence-fill"
                      :style="{ width: (playerStats.hp / playerStats.max_hp) * 100 + '%' }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Головний Кристал Сили (компактніший) -->
            <div class="stat-crystal power-crystal">
              <div class="text-center">
                <div class="stat-mystical-icon text-3xl mb-2">🔮</div>
                <div class="stat-label">Сила Математичної Магії</div>
                <div class="power-value">{{ playerStats.math_power }}</div>
                <!-- Сузір'я Сили -->
                <div class="power-constellation">
                  <div
                    v-for="i in Math.min(playerStats.math_power, 12)"
                    :key="`power-star-${i}`"
                    class="power-star"
                    :style="{ '--delay': i * 0.1 + 's' }"
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Портал до Битви (компактніший) -->
        <div class="battle-nexus">
          <RouterLink to="/battle" class="arithmancer-seal">
            <div class="seal-content">
              <span class="seal-symbol">⚔️</span>
              <div class="seal-text">ВИПРОБУВАННЯ ЧЕКАЄ</div>
              <div class="seal-whisper">Активувати спадкову магію</div>
            </div>
          </RouterLink>
        </div>
      </div>

      <!-- Стан помилки -->
      <div v-else class="sanctum-loading">
        <div class="text-3xl mb-3 text-warning-amber">⚠️</div>
        <div class="loading-inscription text-warning-amber">Зв'язок зі Спадщиною втрачено</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Мінімальні додаткові стилі, що не можуть бути в Tailwind */
.mystical-particle {
  left: calc(var(--start-x, 50%) - 20px + random() * 40px);
}

.floating-rune {
  animation-duration: calc(15s + var(--variance, 0s));
  animation-timing-function: ease-in-out;
}

/* Додаткова анімація для особливої атмосфери */
@keyframes heritageShimmer {
  0%,
  100% {
    background-position: -200% center;
  }
  50% {
    background-position: 200% center;
  }
}

.heritage-name {
  background: linear-gradient(90deg, #f4a460, #d4af37, #f4a460);
  background-size: 200% auto;
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: heritageShimmer 3s infinite;
}

/* Додаткові мобільні оптимізації */
@media (max-height: 700px) {
  .sanctum-title {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
  }

  .sanctum-subtitle {
    font-size: 1rem;
    margin-bottom: 1rem;
  }

  .sanctum-welcome {
    margin-bottom: 1.5rem;
  }

  .wisdom-panel {
    margin-bottom: 1rem;
  }

  .battle-nexus {
    margin-top: 1.5rem;
  }
}

/* Для дуже низьких екранів */
@media (max-height: 600px) {
  .sanctum-content-wrapper {
    padding: 0.5rem;
    padding-top: 0.25rem;
  }

  .wisdom-grid {
    gap: 0.75rem;
  }

  .stat-crystal {
    padding: 0.75rem;
  }
}
</style>
