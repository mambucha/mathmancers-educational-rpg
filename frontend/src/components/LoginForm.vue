<template>
  <div class="login-form p-4 border rounded-lg shadow-md">
    <h2 class="text-xl font-bold mb-4">Login</h2>

    <form @submit.prevent="login">
      <div class="mb-3">
        <label class="block mb-1">Username</label>
        <input v-model="username" type="text" class="w-full border p-2 rounded" required />
      </div>

      <div class="mb-3">
        <label class="block mb-1">Password</label>
        <input v-model="password" type="password" class="w-full border p-2 rounded" required />
      </div>

      <button
        type="submit"
        class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition"
      >
        Login
      </button>
    </form>

    <p v-if="errorMessage" class="text-red-500 mt-2">{{ errorMessage }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth' // 1. Імпортуємо наше сховище
import { useRouter } from 'vue-router' // <-- ДОДАНО

const authStore = useAuthStore() // 2. Ініціалізуємо його
const router = useRouter() // <-- ДОДАНО

const username = ref('')
const password = ref('')
const errorMessage = ref('')

async function login() {
  const params = new URLSearchParams()
  params.append('username', username.value)
  params.append('password', password.value)

  try {
    const response = await axios.post('http://127.0.0.1:8000/api/v1/token', params)

    // 3. Використовуємо дію зі сховища, щоб зберегти токен
    authStore.setToken(response.data.access_token)

    router.push({ name: 'sanctum' }) // <-- НА РЕДІРЕКТ
    errorMessage.value = ''
    // У майбутньому тут буде перенаправлення на сторінку гри
  } catch (err) {
    if (err.response && err.response.status === 401) {
      errorMessage.value = "Неправильне ім'я користувача або пароль"
    } else {
      errorMessage.value = 'Сталася помилка при спробі входу.'
    }
  }
}
</script>
