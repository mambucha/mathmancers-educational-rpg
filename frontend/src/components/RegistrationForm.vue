<script setup>
import { ref } from 'vue'
import axios from 'axios'

const username = ref('') // Додаємо стан для username
const email = ref('')
const password = ref('')
const message = ref('')

const handleSubmit = async () => {
  // Очищуємо попереднє повідомлення
  message.value = ''
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/v1/users/', {
      username: username.value, // Відправляємо username
      email: email.value,
      password: password.value,
    })
    message.value = `Користувача ${response.data.username} успішно створено!`
  } catch (error) {
    if (error.response && error.response.data && error.response.data.detail) {
      message.value = `Помилка: ${error.response.data.detail}`
    } else {
      message.value = 'Сталася невідома помилка.'
    }
  }
}
</script>

<template>
  <div class="registration-form">
    <h1>Реєстрація</h1>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="username">Ім'я користувача:</label>
        <input type="text" id="username" v-model="username" required />
      </div>

      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required />
      </div>

      <div class="form-group">
        <label for="password">Пароль:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit">Зареєструватися</button>
    </form>
    <p v-if="message" class="message">{{ message }}</p>
  </div>
</template>

<style scoped>
.registration-form {
  max-width: 400px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
.form-group {
  margin-bottom: 15px;
}
label {
  display: block;
  margin-bottom: 5px;
}
input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
  border: 1px solid #ddd;
  border-radius: 4px;
}
button {
  width: 100%;
  padding: 10px;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}
button:hover {
  background-color: #33a06f;
}
.message {
  margin-top: 15px;
  color: red; /* Робимо текст помилки червоним */
}
</style>
