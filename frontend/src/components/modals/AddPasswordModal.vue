<template>
  <div id="addPasswordModal">
    <div class="close-button" v-on:click="closePasswordModal"></div>
    <div class="form" id="addPasswordModalForm">
      <h2 class="form-title">Add Password</h2>
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
          v-model="password_content"
        />
        <div class="passwordFieldIcon" v-on:click="togglePasswordVisibility"></div>
      </div>
      <input
        class="input-field"
        type="text"
        id="passwordUsernameInput"
        placeholder="Password Username"
        v-model="password_username"
      />
      <input
        class="input-field"
        type="text"
        id="passwordUrlInput"
        placeholder="Password Url"
        v-model="password_url"
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
      </div>
      <category-list />
      <a class="add-cat-button" v-on:click="openAddCategoryModal">Add a New Category</a>
      <span class="buttons">
        <div class="check-boxes">
          <label for="numberCheck">Include Numbers:</label>
          <input class="checkbox" v-model="includeNumbers" name="numberCheck" type="checkbox" />
          <label for="symbolCheck">Include Symbols:</label>
          <input class="checkbox" v-model="includeSymbols" type="checkbox" />
        </div>
        <button class="main-button" v-on:click="generatePassword" id="generatePasswordButton">Generate</button>
        <button :class="{'main-button': !passwordAddSuccess, 'success-button': passwordAddSuccess}" v-on:click="submitPasswordForm" id="submitPasswordButton">{{ passwordAddSuccess ? 'Added' : 'Add' }}</button>
      </span>
    </div>
    <div class="overlay"></div>
    <add-category-modal v-if="addCategoryModalVisible" />
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
  data() {
    return {
      length: 16,
      password_username: "",
      password_url: "",
      password_content: "",
      category: Object,
      addCategoryModalVisible: false,
      passwordAddSuccess: false,
      includeSymbols: false,
      includeNumbers: false,
    };
  },
  methods: {
    generatePassword() {
      var session = JSON.parse(window.sessionStorage.vuex);
      axios
        .post(BACKEND_URI + "/api/GeneratePassword", {
          session_key: session.session_key,
          user_key: session.user.user_key,
          include_symbols: this.includeSymbols,
          include_numbers: this.includeNumbers,
          length: this.length,
        })
        .then((response) => {
          this.password_content = response.data.password;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    submitPasswordForm() {
      var session = JSON.parse(window.sessionStorage.vuex);
      axios
        .post(BACKEND_URI + "/api/CreatePassword", {
          session_key: session.session_key,
          user_key: session.user.user_key,
          password: {
            ref_category_key: this.category.category_key,
            ref_user_key: session.user.user_key,
            password_content: this.password_content,
            password_username: this.password_username,
            password_url: this.password_url,
            password_category: this.password_category
          },
        })
        .then(() => {this.passwordAddSuccess = true;})
        .catch((error) => {
          console.log(error);
          this.passwordAddSuccess = false;
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
      EventBus.$emit("close-add-password-modal");
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
    this.generatePassword();
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
@import "../../assets/scss/add-password-modal.scss";
</style>