<template>
  <span class="password">
    <h3>{{ password.password_url }}</h3>
    <p>{{ password.password_username }}</p>
  </span>
</template>

<script>
export default {
  props: {
      password: Object
  }
};
</script>

<style scoped>
@import "../../assets/scss/password.scss";
</style>