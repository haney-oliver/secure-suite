<template>
  <div class="navbar">
    <span class="title">SECURE SUITE</span>
    <ul class="options">
      <li>
        <router-link to="/">Home</router-link>
      </li>
      <li>
        <router-link to="/quickstart">Quickstart</router-link>
      </li>
      <li v-show="user">
        <router-link to="/dashboard">Dashboard</router-link>
      </li>
      <li v-show="user">
        <router-link to="/vault">Vault</router-link>
      </li>
      <li v-show="user">
        <router-link to="/preferences">Preferences</router-link>
      </li>
      <li v-if="user">
        <a @click="logOut">Logout</a>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import { EventBus } from "@/event-bus";
import axios from "axios";
import { BACKEND_URI } from "../main";
import store from "../store";
import router from "../router";

export default {
  name: "Navbar",
  data() {
    return {
      showList: false
    };
  },
  methods: {
    logOut() {
      var session = JSON.parse(window.sessionStorage.vuex);
      axios
        .post(BACKEND_URI + "/api/LogoutUser", {
          user_key: session.user.user_key,
          session_key: session.session_key
        })
        .then(() => {
          store.dispatch("removeUserAndSession");
          router.replace("/login");
        })
        .catch(response => console.log(response.message));
    },
    scrollTo(ref) {
      EventBus.$emit("scroll-to", ref);
    }
  },
  computed: {
    ...mapGetters({
      user: "user"
    })
  }
};
</script>

<style scoped lang="scss">
@import "@/assets/scss/navbar.scss";
</style>
