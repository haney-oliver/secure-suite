<template>
  <router-view />
</template>

<script>
import router from "@/router/index";
export default {
  mounted() {
    router.replace("/login");
  }
}
</script>

<style>
html {
  width: 400px;
  height: 500px;
  overflow-y: scroll;
  scrollbar-width: thin;
  scrollbar-color:#6480ff  #ebebeb;
}

body {
  width: 400px;
  overflow-x: hidden;
}
</style>
