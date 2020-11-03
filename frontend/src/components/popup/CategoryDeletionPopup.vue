<template>
  <div id="categoryDeletionPopup">
    <div class="close-button" v-on:click="closeCategoryDeletionPopup"></div>
    <div class="form" id="categoryDeletionPopupForm">
      <h2 class="form-title">Are you sure you want to delete category?</h2>
      <p class="warning">Warning! This will delete all passwords in the category!</p>
      <span class="buttons">
        <progress-button fillColor="#ffffff" :height="5" position="bottom" class="danger" v-on:click="deleteCategory" id="deleteCategoryButton">Delete</progress-button>
      </span>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { BACKEND_URI } from "@/main";
import { EventBus } from "@/event-bus";
import Button from 'vue-progress-button'

export default {
  components: {
    "progress-button": Button
  },
  props: {
    category: Object
  },
  methods: {
    deleteCategory() {
      var session = JSON.parse(window.sessionStorage.vuex);
      axios
        .post(BACKEND_URI + "/api/DeleteCategory", {
          session_key: session.session_key,
          user_key: session.user.user_key,
          category_key: this.category.category_key,
        }).then(this.closeCategoryDeletionPopup())
        .catch((error) => {
          console.log(error);
        });
    },
    closeCategoryDeletionPopup() {
      EventBus.$emit("close-delete-category-popup")
    }
  }
};
</script>

<style scoped>
@import "../../assets/scss/category-deletion-popup.scss";
</style>