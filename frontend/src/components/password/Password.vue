<template>
  <span class="password">
    <h3>{{ password.password_url }}</h3>
    <p>{{ password.password_username }}</p>
  </span>
</template>

<script>
export default {
  props: [password]
};
</script>

<style scoped>
</style>