<template>
  <div id="passwordDeletionPopup">
    <div class="close-button" v-on:click="closePasswordDeletionPopup"></div>
    <div class="form" id="passwordDeletionPopupForm">
      <h2 class="form-title">Are you sure you want to delete password?</h2>
      <span class="buttons">
        <button :height="5" position="bottom" :class="{'danger': !passwordDeleteSuccess, 'success-button': passwordDeleteSuccess}" v-on:click="deletePassword" id="deletePasswordButton">{{ passwordDeleteSuccess ? 'Deleted' : 'Delete' }}</button>
      </span>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { BACKEND_URI } from "@/main";
import { EventBus } from "@/event-bus";

export default {
  props: {
    password: Object
  },
  data() {
    return {
      passwordDeleteSuccess: false
    }
  },
  methods: {
    deletePassword() {
      var session = JSON.parse(window.sessionStorage.vuex);
      axios
        .post(BACKEND_URI + "/api/DeletePassword", {
          session_key: session.session_key,
          user_key: session.user.user_key,
          password_key: this.password.password_key,
        })
        .then(() => {
            this.passwordDeleteSuccess = true;
        })
        .catch((error) => {
          console.log(error);
          this.passwordDeleteSuccess = false;
        });
    },
    closePasswordDeletionPopup() {
      EventBus.$emit("close-delete-password-popup")
    }
  }
};
</script>

<style scoped>
@import "../../assets/scss/password-deletion-popup.scss";
</style>