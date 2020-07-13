<template>
  <div id="addPasswordModal">
    <div class="xButton" v-on:click="closePasswordModal"></div>
    <div class="form" id="addPasswordModalForm">
      <h2 class="formTitle">Add Password</h2>
      <div class="iconSearchField">
        <input
          class="inputField"
          type="password"
          id="passwordContentInput"
          placeholder="Password Content"
          v-model="password_content"
        />
        <div class="searchFieldIcon" v-on:click="togglePasswordVisibility"></div>
      </div>
      <input
        class="inputField"
        type="text"
        id="passwordUsernameInput"
        placeholder="Password Username"
        v-model="password_username"
      />
      <input
        class="inputField"
        type="text"
        id="passwordCategoryInput"
        placeholder="Password Category"
        v-model="password_category"
      />
      <input
        class="inputField"
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
      <button v-on:click="generatePassword" id="generatePasswordButton">Generate</button>
      <button v-on:click="submitPasswordForm" id="submitPasswordForm">Add</button>
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
      password_username: String,
      password_url: String,
      password_content: String,
      ref_category_key: String
    };
  },
  methods: {
    generatePassword() {
      var passwordField = document.getElementById("passwordContentInput");
      axios
        .post(BACKEND_URI + "/api/GeneratePassword", {
          length: this.length
        })
        .then(response => {
          var code = response.data.status;
          passwordField.value = response.data.generatedPassword;
        })
        .catch(error => {
          console.log(error);
        });
    },
    submitPasswordForm() {
      axios
        .post(BACKEND_URI + "/api/CreatePassword", {
          user_key: "",
          session_key: "",
          password: {
            ref_user_key: this.$route.params.userId,
            password_name: document.getElementById("passwordNameInput").value,
            password_content: document.getElementById("passwordContentInput")
              .value,
            password_username: document.getElementById("passwordUsernameInput")
              .value,
            password_url: document.getElementById("passwordUrlInput").value,
            password_category: document.getElementById("passwordCategoryInput")
              .value
          }
        })
        .then(response => {
          this.closePasswordModal();
        })
        .catch(error => {
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
      this.$emit("close");
    }
  },
  watch: {
    length: function() {
      this.generatePassword();
    }
  }
};
</script>

<style scoped>
@import "../../assets/scss/add-password-modal.scss"
</style>