<script setup>
import { ref } from "vue"
import api from "../services/api"

const email = ref("")
const password = ref("")

const login = async () => {

  try {

    const response = await api.post(
      "/auth/login",
      {
        email: email.value,
        password: password.value
      }
    )

    console.log(response.data)

    localStorage.setItem(
      "token",
      response.data.access_token
    )

    alert("Login berhasil!")

  } catch (error) {

    console.log(error)

    alert("Login gagal")
  }
}
</script>

<template>

  <div>

    <h1>Login</h1>

    <input
      v-model="email"
      placeholder="Email"
    />

    <input
      v-model="password"
      type="password"
      placeholder="Password"
    />

    <button @click="login">
      Login
    </button>

  </div>

</template>