<template>
  <div id="editPasswordModal">
    <div class="close-button" v-on:click="closePasswordModal"></div>
    <div class="form" id="editPasswordModalForm">
      <h2 class="form-title">Edit Password</h2>
      <input
          class="input-field"
          type="text"
          id="categoryInput"
          placeholder="Select a Category"
          v-model="category.category_name"
          disabled
      />
      <div class="icon-input-field">
        <input
          type="password"
          id="passwordContentInput"
          placeholder="Password Content"
          v-model="password.password_content"
        />
        <div class="passwordFieldIcon" v-on:click="togglePasswordVisibility"></div>
      </div>
      <input
        class="input-field"
        type="text"
        id="passwordUsernameInput"
        placeholder="Password Username"
        v-model="password.password_username"
      />
      <input
        class="input-field"
        type="text"
        id="passwordUrlInput"
        placeholder="Password Url"
        v-model="password.password_url"
      />
      <div class="slidecontainer">
        <input
          type="range"
          min="1"
          max="50"
          value="25"
          class="slider"
          id="lengthSlider"
          v-model="length"
        />
        <h2 id="sliderValue">Password Length: {{ length }}</h2>
        <category-list />
        <a class="add-cat-button" v-on:click="openAddCategoryModal">Add a New Category</a>
      </div>
      <span class="buttons">
        <button class="main-button" v-on:click="generatePassword" id="generatePasswordButton">Generate</button>
        <button :class="{'main-button': !updatePasswordSuccess, 'success-button': updatePasswordSuccess}" v-on:click="submitPasswordForm" id="submitPasswordButton">{{ updatePasswordSuccess ? 'Updated' : 'Update' }}</button>
      </span>
    </div>
    <add-category-modal v-if="addCategoryModalVisible"/>
  </div>
</template>

<script>
import axios from "axios";
import { BACKEND_URI } from "@/main";
import { EventBus } from "@/event-bus";
import CategoryList from "@/components/category/CategoryList"
import AddCategoryModal from "@/components/modals/AddCategoryModal"

export default {
  components: {
    CategoryList,
    AddCategoryModal
  },
  props: {
    passwordKey: String
  },
  data() {
    return {
      length: 16,
      password: Object,
      category: Object,
      addCategoryModalVisible: false,
      addCategoryModalKey: 0,
      updatePasswordSuccess: false,
    };
  },
  methods: {
    getCategory() {
      var session = JSON.parse(window.sessionStorage.vuex);
      axios
        .post(BACKEND_URI + "/api/GetCategory", {
          session_key: session.session_key,
          user_key: session.user.user_key,
          category_key: this.password.ref_category_key
        })
        .then((response) => {
          this.category = response.data.category;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getPassword() {
      var session = JSON.parse(window.sessionStorage.vuex);
      axios
        .post(BACKEND_URI + "/api/GetPassword", {
          session_key: session.session_key,
          user_key: session.user.user_key,
          password_key: this.passwordKey
        })
        .then((response) => {
          this.password = response.data.password;
          this.getCategory();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    generatePassword() {
      var session = JSON.parse(window.sessionStorage.vuex);
      axios
        .post(BACKEND_URI + "/api/GeneratePassword", {
          session_key: session.session_key,
          user_key: session.user.user_key,
          length: this.length,
        })
        .then((response) => {
          this.password.password_content = response.data.password;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    submitPasswordForm() {
      var session = JSON.parse(window.sessionStorage.vuex);
      axios
        .post(BACKEND_URI + "/api/UpdatePassword", {
          session_key: session.session_key,
          user_key: session.user.user_key,
          password_key: this.password.password_key,
          password: {
            ref_user_key: session.user.user_key,
            password_content: this.password.password_content,
            password_username: this.password.password_username,
            password_url: this.password.password_url,
            ref_category_key: this.category.category_key
          },
        })
        .then(this.updatePasswordSuccess = true)
        .catch((error) => {
          console.log(error);
          this.updatePasswordSuccess = false;
        });
    },
    togglePasswordVisibility() {
      var x = document.getElementById("passwordContentInput");
      if (x.type === "password") {
        x.type = "text";
      } else {
        x.type = "password";
      }
    },
    closePasswordModal() {
      EventBus.$emit("close-edit-password-modal");
    },
    openAddCategoryModal() {
      this.addCategoryModalVisible = true;
    }
  },
  watch: {
    length: function () {
      this.generatePassword();
    },
  },
  mounted() {
    this.getPassword();
    EventBus.$on("category-clicked", e => {
      this.category = e;
    })
    EventBus.$on("close-add-category-modal", () => {
      this.addCategoryModalVisible = false;
    })
  },
};
</script>

<style scoped>
@import "../../assets/scss/edit-password-modal.scss";
</style>