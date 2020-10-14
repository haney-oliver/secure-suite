<template>
  <span class="password" @click="emitPassword">
    <h3>{{ password.password_url }}</h3>
    <p>{{ password.password_username }}</p>
  </span>
</template>

<script>
import { EventBus } from "@/event-bus";
export default {
  props: {
      password: Object
  },
  methods: {
    emitPassword() {
      EventBus.$emit("password-clicked", this.password);
    }
  }
};
</script>

<style scoped>
@import "../../assets/scss/password.scss";
</style>