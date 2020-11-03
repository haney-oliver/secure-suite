<template>
  <span class="password" @click.self="emitPassword" @mouseover="showX = true" @mouseleave="showX = false">
    <transition name="fade">
      <div @click.stop.prevent="openPasswordDeletionPopup" class="close-button" v-show="showX"></div>
    </transition>
    <h3 class="password-url">{{ password.password_url }}</h3>
    <p class="password-username">{{ password.password_username }}</p>
    <password-deletion-popup :password="password" v-show="passwordDeletionPopupVisible" />
  </span>
</template>

<script>
import { EventBus } from "@/event-bus";
import PasswordDeletionPopup from "@/components/popup/PasswordDeletionPopup"
export default {
  components: {
    PasswordDeletionPopup
  },
  data() {
    return {
      showX: false,
      passwordDeletionPopupVisible: false
    }
  },
  props: {
      password: Object
  },
  methods: {
    emitPassword() {
      EventBus.$emit("password-clicked", this.password);
    },
    openPasswordDeletionPopup() {
      this.passwordDeletionPopupVisible = true;
    }
  },
  mounted() {
    EventBus.$on("close-delete-password-popup", () => {
      this.passwordDeletionPopupVisible = false;
    })
  }
};
</script>

<style scoped>
@import "../../assets/scss/password.scss";
</style>