<template>
  <div class="register-view">
    <navbar />
    <div class="area">
      <ul class="circles">
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
      </ul>
    </div>
    <div class="container">
      <div class="form" id="registerForm">
        <h2 class="form-title">Register</h2>
        <input class="input-field" type="text" v-model="username" placeholder="Username" />
        <input class="input-field" type="email" v-model="userEmail" placeholder="Email" />
        <input class="input-field" type="password" v-model="userPassword" placeholder="Password" />
        <span class="buttons">
          <button class="main-button" v-on:click="register" id="registerButton">
            <span class="button-content">Register</span>
          </button>
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from "@/components/Navbar";
import axios from "axios";
import { BACKEND_URI } from "@/main";
import router from "@/router/index";

export default {
  name: "RegisterView",
  components: {
    navbar: Navbar
  },
  data() {
    return {
      username: null,
      userPassword: null,
      userEmail: null
    };
  },
  methods: {
    register() {
      axios
        .post(BACKEND_URI + "/api/RegisterUser", {
          user: {
            user_name: this.username,
            user_email: this.userEmail,
            user_password: this.userPassword
          }
        })
        .then(() => {
          router.replace("/login");
        })
        .catch(error => console.log(error.message));
    }
  }
};
</script>

<style scoped lang="scss">
@import "@/assets/scss/register-view.scss";
</style>