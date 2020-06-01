<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
import store from "./store";

export default {
  name: "App",
  onIdle() {
    store.dispatch("removeUser");
  }
};
</script>

<style>
</style>
