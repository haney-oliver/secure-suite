<template>
  <div id="preferencesModal">
    <div class="close-button" v-on:click="closePreferencesModal"></div>
    <div class="form" id="preferencesModalForm">
      <h2 class="form-title">User Settings</h2>
      <h4 class="label">Username</h4>
      <input
          class="input-field"
          type="text"
          id="usernameInput"
          v-model="username"
      />
      <h4 class="label">User Password</h4>
      <div class="icon-input-field">
        <input
          type="password"
          id="passwordInput"
          v-model="userPassword"
        />
        <div class="passwordFieldIcon" v-on:click="togglePasswordVisibility"></div>
      </div>
      <h4 class="label">User Email</h4>
      <input
          class="input-field"
          type="text"
          id="userEmailInput"
          v-model="userEmail"
      />
      <span class="buttons">
        <button class="main-button" v-on:click="updateUser" id="updateUserButton">Save</button>
      </span>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { BACKEND_URI } from "@/main";
import { EventBus } from "@/event-bus";

export default {
  data() {
    return {
      session: Object,
      username: "",
      userPassword: "",
      userEmail: ""
    };
  },
  methods: {
    updateUser() {
      axios
        .post(BACKEND_URI + "/api/UpdateUser", {
          session_key: this.session.session_key,
          user_key: this.session.user.user_key,
          user: {
            user_key: this.session.user.user_key,
            user_password: this.userPassword,
            user_email: this.userEmail 
          },
        })
        .catch((error) => {
          console.log(error);
        });
    },
    togglePasswordVisibility() {
      var x = document.getElementById("passwordInput");
      if (x.type === "password") {
        x.type = "text";
      } else {
        x.type = "password";
      }
    },
    closePreferencesModal() {
      EventBus.$emit("close-preferences-modal");
    },
  },
  mounted() {
    this.session = JSON.parse(window.sessionStorage.vuex);
    this.username = this.session.user.user_name;
    this.userPassword = this.session.user.user_key;
    this.userEmail = this.session.user.user_email;
  }
};
</script>

<style scoped>
@import "../../assets/scss/preferences-modal.scss";
</style>
