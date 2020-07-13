<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
import axios from "axios";
import { BACKEND_URI } from "@/main";
import store from "@/store";
import router from "@/router/index";

export default {
  name: "App",
  onIdle() {
    var session = JSON.parse(window.sessionStorage.vuex);
    axios
      .post(BACKEND_URI + "/api/LogoutUser", {
        user_key: session.user.user_key,
        session_key: session.session_key
      })
      .then(() => {
        store.dispatch("removeUserAndSession");
        router.replace("/");
      })
      .catch(error => console.log(error.message));
  }
};
</script>

<style lang="scss">
@import "assets/scss/_base.scss";
</style>
