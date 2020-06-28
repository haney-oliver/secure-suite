<template>
  <div class="LoginPage" id="loginPage">
    <navbar />
    <div class="container">
      <div class="form" id="loginForm">
        <h2 class="formTitle">Login</h2>
        <input
          class="inputField"
          type="text"
          v-model="usernameOrEmail"
          placeholder="Enter email or username"
        />
        <input class="inputField" type="password" v-model="userPassword" placeholder="Password" />
        <button class="main-button" v-on:click="login" id="loginButton">Login</button>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from "@/components/Navbar";
import axios from "axios";
import { BACKEND_URI } from "@/main";
import store from "@/store";
import router from "@/router/index";

export default {
  name: "LoginPage",
  components: {
    navbar: Navbar
  },
  data() {
    return {
      usernameOrEmail: null,
      userPassword: null
    };
  },
  methods: {
    login() {
      axios
        .post(BACKEND_URI + "/api/LoginUser", {
          userNameOrEmail: this.usernameOrEmail,
          userPassword: this.userPassword
        })
        .then(response => {
          store.dispatch("setUser", response.user);
          router.replace("/dashboard");
        })
        .catch(error => console.log(error.message));
    }
  }
};
</script>

<style scoped>
</style>