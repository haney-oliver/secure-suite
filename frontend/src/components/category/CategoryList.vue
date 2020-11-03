<template>
  <div class=container>
    <h4>Catagories</h4>
    <span class="category-list">
    <category-mini
      v-for="category in categories"
      :key="category.category_key" 
      v-bind:category="category"
    />
  </span>
  </div>
</template>

<script>
import axios from "axios";
import { BACKEND_URI } from "@/main";
import CategoryMini from "@/components/category/CategoryMini"
import { EventBus } from "@/event-bus"

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
          console.log(response.data.categories)
          this.categories.sort();
          this.$forceUpdate();
        })
        .catch(err => {
          console.log(err);
        });
    }
  },
  mounted() {
    this.fetchCategories();
    EventBus.$on("close-add-category-modal", () => {
      this.fetchCategories();
      this.$forceUpdate();
    })
  }
};
</script>

<style scoped>
@import "../../assets/scss/category-list.scss";
</style>