<template>
  <div id="categoryDeletionPopup">
    <div class="close-button" v-on:click="closeCategoryDeletionPopup"></div>
    <div class="form" id="categoryDeletionPopupForm">
      <h2 class="form-title">Are you sure you want to delete category?</h2>
      <p class="warning">Warning! This will delete all passwords in the category!</p>
      <span class="buttons">
        <button fillColor="#ffffff" :height="5" position="bottom" :class="{'danger': !categoryDeleteSuccess, 'success-button': categoryDeleteSuccess}" v-on:click="deleteCategory" id="deleteCategoryButton">{{ categoryDeleteSuccess ? 'Deleted' : 'Delete' }}</button>
      </span>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { BACKEND_URI } from "@/main";
import { EventBus } from "@/event-bus";

export default {
  props: {
    category: Object
  },
  data() {
    return {
      categoryDeleteSuccess: false
    }
  },
  methods: {
    deleteCategory() {
      var session = JSON.parse(window.sessionStorage.vuex);
      axios
        .post(BACKEND_URI + "/api/DeleteCategory", {
          session_key: session.session_key,
          user_key: session.user.user_key,
          category_key: this.category.category_key,
        }).then(this.categoryDeleteSuccess = true)
        .catch((error) => {
          console.log(error);
          this.categoryDeleteSuccess = false;
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