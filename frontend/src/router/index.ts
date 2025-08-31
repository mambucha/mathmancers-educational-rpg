import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import BattleView from '../views/BattleView.vue' // 1. Імпортуємо нову сторінку
import { useAuthStore } from '@/stores/auth' // 2. Імпортуємо наше сховище
import SanctumView from '../views/SanctumView.vue' // <-- ДОДАНО

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/battle', // 3. Створюємо шлях для нашої ігрової сторінки
      name: 'battle',
      component: BattleView,
      meta: { requiresAuth: true }, // 4. Позначаємо, що ця сторінка потребує входу
    },
    {
      path: '/sanctum', // <-- ДОДАНО НОВИЙ РОУТ
      name: 'sanctum',
      component: SanctumView,
      meta: { requiresAuth: true },
    },
  ],
})

// 5. Ось наш "викидайло"!
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // Перевіряємо, чи сторінка потребує автентифікації І чи користувач не залогінений
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // Якщо так - відправляємо його на головну сторінку для логіну
    next({ name: 'home' })
  } else {
    // Інакше - пропускаємо
    next()
  }
})

export default router
