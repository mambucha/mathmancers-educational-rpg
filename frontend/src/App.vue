<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const handleLogout = () => {
  authStore.logout()
  // Після виходу перенаправляємо на головну сторінку
  router.push({ name: 'home' })
}
</script>

<template>
  <header>
    <nav>
      <RouterLink to="/">Головна</RouterLink>
      <RouterLink to="/battle">Почати бій</RouterLink>
      <button v-if="authStore.isAuthenticated" @click="handleLogout">Вийти</button>
    </nav>
  </header>

  <main>
    <RouterView />
  </main>
</template>

<style scoped>
header {
  background-color: #f3f3f3;
  padding: 1rem;
  border-bottom: 1px solid #ddd;
}
nav {
  display: flex;
  gap: 1rem;
  align-items: center;
}
nav a {
  text-decoration: none;
  color: #333;
}
nav button {
  margin-left: auto; /* Розміщує кнопку справа */
  cursor: pointer;
}
</style>
