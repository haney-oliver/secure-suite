<template>
  <span v-if="showCat" class="category" v-bind:style="{'background-color': color}" @mouseover="showX=true" @mouseleave="showX=false">
    <transition name="fade">
      <div v-on:click="openCategoryDeletionPopup" class="close-button" v-show="showX"></div>
    </transition>  
    <h3 class="category-name">{{ category.category_name }}</h3>
    <password
      v-for="password in passwords"
      :key="password.password_key"
      v-bind:password="password"
    />
    <category-deletion-popup :category=category v-if="categoryDeletionPopupVisible"/>
  </span>
</template>

<script>
import axios from "axios";
import { BACKEND_URI } from "@/main";
import Password from "@/components/password/Password.vue";
import CategoryDeletionPopup from "@/components/popup/CategoryDeletionPopup"
import { EventBus } from '../../event-bus';

export default {
  props: {
    category: Object,
    color: String
  },
  data() {
    return {
      passwords: [],
      showX: false,
      showCat: false,
      categoryDeletionPopupVisible: false
    };
  },
  components: {
    password: Password,
    CategoryDeletionPopup
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
          if (response.data.passwords == 0) {
            this.showCat = false;
          } else {
            this.showCat = true;
          }
        })
        .catch(err => {
          console.log(err);
        });
    },
    openCategoryDeletionPopup() {
      this.categoryDeletionPopupVisible = true;
    }
  },
  mounted() {
    EventBus.$emit("category-mounted");
    this.fetchPasswords();

    EventBus.$on("close-delete-category-popup", () => {
      this.categoryDeletionPopupVisible = false;
    })
    EventBus.$on("close-delete-password-popup",() => {
      setTimeout(2000)
      this.fetchPasswords()
      this.$forceUpdate();
    })
    EventBus.$on("close-add-password-modal",() => {
      setTimeout(2000)
      this.fetchPasswords();
      this.$forceUpdate();
    })
    EventBus.$on("close-edit-password-modal",() => {
      setTimeout(2000)
      this.fetchPasswords();
      this.$forceUpdate();
    })
  }
};
</script>

<style scoped>
@import "../../assets/scss/category.scss";
</style>