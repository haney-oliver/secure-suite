<template>
  <div class="login-view">
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
      <div class="form" id="loginForm">
        <h2 class="form-title">Login</h2>
        <input class="input-field" type="text" v-model="username" placeholder="Username" />
        <input class="input-field" type="password" v-model="userPassword" placeholder="Password" />
        <span class="buttons">
          <button class="main-button" v-on:click="login" id="loginButton">
            <span class="button-content">Login</span>
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
import store from "@/store";
import router from "@/router/index";

export default {
  name: "LoginPage",
  components: {
    navbar: Navbar
  },
  data() {
    return {
      username: null,
      userPassword: null
    };
  },
  methods: {
    login() {
      if (
        window.sessionStorage.vuex == null ||
        window.sessionStorage.vuex.session == null ||
        window.sessionStorage.vuex.session.session_key == null ||
        window.sessionStorage.vuex.session.user == null
      ) {
        axios
          .post(BACKEND_URI + "/api/LoginUser", {
            user_name: this.username,
            user_password: this.userPassword
          })
          .then(response => {
            var data = {
              user: response.data.user,
              session_key: response.data.session.session_key
            };
            store.dispatch("setUserAndSession", data);
            router.replace("/dashboard");
          })
          .catch(error => console.log(error.message));
      }
    }
  }
};
</script>

<style scoped lang="scss">
@import "@/assets/scss/login-view.scss";
</style>