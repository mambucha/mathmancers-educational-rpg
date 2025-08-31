import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

// Створюємо екземпляр axios з базовими налаштуваннями
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Це "перехоплювач", який додає наш токен до кожного запиту
apiClient.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers['Authorization'] = `Bearer ${authStore.token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

// Експортуємо функції для кожного типу запиту
export default {
  startBattle() {
    return apiClient.get('/battle/start')
  },

  // ОНОВЛЕНА функція submitAnswer з підтримкою операцій для алгебри
  submitAnswer(enemyId, problemObject, answer = null, operation = null) {
    const payload = {
      enemy_id: enemyId,
      problem: problemObject,
      answer: answer,
      operation: operation,
    }

    console.log('Sending to server:', payload) // Для налагодження

    return apiClient.post('/battle/answer', payload)
  },

  getPlayerStats() {
    return apiClient.get('/player/me')
  },
  healPlayer() {
    return apiClient.post('/player/heal')
  },
}
