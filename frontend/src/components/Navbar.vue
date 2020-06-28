<template>
  <div class="navbar">
    <ul class="options">
      <li>
        <router-link to="/">Home</router-link>
      </li>
      <li @click="scrollTo('book-trailers')">
        <a href="/#features">Feature</a>
      </li>
      <li @click="scrollTo('quickstart')">
        <a href="/#quickstart">Quickstart</a>
      </li>
      <li v-show="user.loggedIn">
        <router-link to="/dashboard">Dashboard</router-link>
      </li>
      <li v-show="user.loggedIn">
        <router-link to="/vault">Vault</router-link>
      </li>
      <li v-show="user.loggedIn">
        <router-link to="/preferences">Preferences</router-link>
      </li>
      <li v-if="user.loggedIn">
        <a @click.prevent="signOut">Logout</a>
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

export default {
  name: "Navbar",
  data() {
    return {
      showList: false
    };
  },
  methods: {
    signOut() {
      axios
        .post(BACKEND_URI + "/api/LogoutUser", {
          user_key: store.state.user_key
        })
        .then(store.dispatch("fetchUser", null))
        .catch(response => console.log(response.message));
    },
    show() {
      if (this.onBookTrailersPage) {
        this.showList = true;
      }
    },
    hide() {
      this.showList = false;
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

<style scoped>
</style>
