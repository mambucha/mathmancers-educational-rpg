import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// 'useAuthStore' - це назва нашого сховища
export const useAuthStore = defineStore('auth', () => {
  // **State (Стан)**: Тут зберігаються наші дані
  const token = ref(localStorage.getItem('access_token')) // Одразу намагаємось завантажити токен

  // **Actions (Дії)**: Функції, які змінюють стан
  function setToken(newToken) {
    localStorage.setItem('access_token', newToken)
    token.value = newToken
  }

  function logout() {
    localStorage.removeItem('access_token')
    token.value = null
  }

  // **Getters (Отримувачі)**: Функції, які повертають дані зі стану або обчислюють їх
  const isAuthenticated = computed(() => {
    return token.value !== null
  })

  // Повертаємо все, що має бути доступним ззовні
  return { token, setToken, logout, isAuthenticated }
})
