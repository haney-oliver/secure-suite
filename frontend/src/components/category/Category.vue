<template>
  <span class="category" v-bind:style="{'background-color': color}">
    <h3>{{ category.category_name }}</h3>
    <password
      v-for="password in passwords"
      :key="password.password_key"
      v-bind:password="password"
    />
  </span>
</template>

<script>
import axios from "axios";
import { BACKEND_URI } from "@/main";
import Password from "@/components/password/Password.vue";

export default {
  props: {
    category: Object,
    color: String
  },
  data() {
    return {
      passwords: []
    };
  },
  components: {
    password: Password
  },
  methods: {
    fetchPasswords() {
      var session = JSON.parse(window.sessionStorage.vuex);
      axios
        .post(BACKEND_URI + "/api/ListPasswords", {
          session_key: session.session_key,
          user_key: session.user.user_key,
          ref_category_key: this.category.category_key
        })
        .then(response => {
          this.passwords = response.data.passwords;
        })
        .catch(err => {
          console.log(err);
        });
    }
  },
  mounted() {
    this.fetchPasswords();
  }
};
</script>

<style scoped>
@import "../../assets/scss/category.scss";
</style>