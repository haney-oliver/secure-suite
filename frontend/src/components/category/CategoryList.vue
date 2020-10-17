<template>
  <span class="category-list">
    <category-mini
      v-for="category in categories"
      :key="category.category_key" 
      v-bind:category="category"
    />
  </span>
</template>

<script>
import axios from "axios";
import { BACKEND_URI } from "@/main";
import CategoryMini from "@/components/category/CategoryMini"

export default {
  props: {
    color: String
  },
  components: {
    CategoryMini
  },
  data() {
    return {
      categories: []
    };
  },
  methods: {
    fetchCategories() {
      var session = JSON.parse(window.sessionStorage.vuex);
      axios
        .post(BACKEND_URI + "/api/ListCategories", {
          session_key: session.session_key,
          user_key: session.user.user_key
        })
        .then(response => {
          this.categories = response.data.categories;
        })
        .catch(err => {
          console.log(err);
        });
    }
  },
  mounted() {
    this.fetchCategories();
  }
};
</script>

<style scoped>
@import "../../assets/scss/category-list.scss";
</style>