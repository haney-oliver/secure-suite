<template>
  <div id="addPasswordModal">
    <div class="close-button" v-on:click="closePasswordModal"></div>
    <div class="form" id="addPasswordModalForm">
      <h2 class="form-title">Add Password</h2>
      <div class="icon-input-field">
        <input
          type="password"
          id="passwordContentInput"
          placeholder="Password Content"
          v-model="password_content"
        />
        <div class="passwordFieldIcon" v-on:click="togglePasswordVisibility"></div>
      </div>
      <input
        class="input-field"
        type="text"
        id="passwordUsernameInput"
        placeholder="Password Username"
        v-model="password_username"
      />
      <input
        class="input-field"
        type="text"
        id="passwordCategoryInput"
        placeholder="Password Category"
        v-model="ref_category_key"
      />
      <input
        class="input-field"
        type="text"
        id="passwordUrlInput"
        placeholder="Password Url"
        v-model="password_url"
      />
      <div class="slidecontainer">
        <input
          type="range"
          min="1"
          max="50"
          value="25"
          class="slider"
          id="lengthSlider"
          v-model="length"
        />
        <h2 id="sliderValue">Password Length: {{ length }}</h2>
      </div>
      <span class="buttons">
        <button v-on:click="generatePassword" id="generatePasswordButton">Generate</button>
        <button v-on:click="submitPasswordForm" id="submitPasswordForm">Add</button>
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
      length: 25,
      password_username: "",
      password_url: "",
      password_content: "",
      ref_category_key: String,
    };
  },
  methods: {
    generatePassword() {
      var session = JSON.parse(window.sessionStorage.vuex);
      var passwordField = document.getElementById("passwordContentInput");
      axios
        .post(BACKEND_URI + "/api/GeneratePassword", {
          session_key: session.session_key,
          user_key: session.user.user_key,
          length: this.length,
        })
        .then((response) => {
          passwordField.value = response.data.password;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    submitPasswordForm() {
      var session = JSON.parse(window.sessionStorage.vuex);
      axios
        .post(BACKEND_URI + "/api/CreatePassword", {
          session_key: session.session_key,
          user_key: session.user.user_key,
          password: {
            ref_user_key: this.$route.params.userId,
            password_name: document.getElementById("passwordNameInput").value,
            password_content: document.getElementById("passwordContentInput")
              .value,
            password_username: document.getElementById("passwordUsernameInput")
              .value,
            password_url: document.getElementById("passwordUrlInput").value,
            password_category: document.getElementById("passwordCategoryInput")
              .value,
          },
        })
        .then(this.closePasswordModal())
        .catch((error) => {
          console.log(error);
        });
    },
    togglePasswordVisibility() {
      var x = document.getElementById("passwordContentInput");
      if (x.type === "password") {
        x.type = "text";
      } else {
        x.type = "password";
      }
    },
    closePasswordModal() {
      EventBus.$emit("close-add-password-modal");
    },
  },
  watch: {
    length: function () {
      this.generatePassword();
    },
  },
  mounted() {
    this.generatePassword();
  },
};
</script>

<style scoped>
@import "../../assets/scss/add-password-modal.scss";
</style>