<template>
  <div id="addCategoryModal">
    <div class="close-button" v-on:click="closeCategoryModal"></div>
    <div class="form" id="addCategoryModalForm">
      <h2 class="form-title">Add Category</h2>
      <input
          class="input-field"
          type="text"
          id="categoryNameInput"
          placeholder="Category Name"
          v-model="category_name"
      />
      <input
        class="input-field"
        type="text"
        id="categoryDescription"
        placeholder="Describe your category"
        v-model="category_desc"
      />
      <span class="buttons">
        <button :class="{'main-button': !categoryAddSuccess, 'success-button': categoryAddSuccess}" v-on:click="submitCategoryForm" id="submitCategoryButton">{{ categoryAddSuccess ? 'Added' : 'Add' }}</button>
      </span>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { BACKEND_URI } from "@/main";
import { EventBus } from "@/event-bus";

export default {
  data() {
    return {
      category_name: "",
      category_desc: "",
      categoryAddSuccess: false
    };
  },
  methods: {
    submitCategoryForm() {
      var session = JSON.parse(window.sessionStorage.vuex);
      axios
        .post(BACKEND_URI + "/api/CreateCategory", {
          session_key: session.session_key,
          user_key: session.user.user_key,
          category: {
            ref_user_key: session.user.user_key,
            category_name: this.category_name,
            category_description: this.category_desc 
          },
        }).then(() => {
          this.categoryAddSuccess = true;
        })
        .catch((error) => {
          console.log(error);
          this.categoryAddSuccess = false;
        });
    },
    toggleCategoryVisibility() {
      var x = document.getElementById("categoryNameInput");
      if (x.type === "category") {
        x.type = "text";
      } else {
        x.type = "category";
      }
    },
    closeCategoryModal() {
      EventBus.$emit("close-add-category-modal");
    },
  }
};
</script>

<style scoped>
@import "../../assets/scss/add-category-modal.scss";
</style>