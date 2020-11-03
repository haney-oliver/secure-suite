<template>
  <span class="vault">
    <navbar />
    <div v-bind:class="{modalopen: modalOpen}"></div>
    <div>
      <div id="searchContainer">
        <input
          transition="slidein"
          type="text"
          class="input-field"
          id="searchField"
          placeholder="Search by category"
          v-model="filter"
        />
      </div>
    </div>
    <span class="vault-buttons buttons">
      <button class="main-button" v-on:click="openAddPasswordModal">
        <span class="button-content">Add New Password</span>
      </button>
    </span>
    <spinner v-if="!categoryMounted" />
    <div class="message">
      <h4 v-if="zeroCategories">You have no passwords. Click "Add New Password" above to get started.</h4>
    </div>
    <category
      v-for="category in renderCategories"
      :key="category.category_key"
      v-bind:category="category"
      v-bind:color="color"
      >{{ chooseColor() }}
    </category>
    <addPasswordModal v-if="addPasswordModalVisible"/>
    <editPasswordModal :passwordKey=passwordKey v-if="editPasswordModalVisible"/>
  </span>
</template>

<script>
import axios from "axios";
import { BACKEND_URI } from "@/main";
import Category from "@/components/category/Category";
import Navbar from "@/components/Navbar";
import AddPasswordModal from "@/components/modals/AddPasswordModal";
import EditPasswordModal from "@/components/modals/EditPasswordModal";
import { EventBus } from "@/event-bus";
import Spinner from "@/components/spinner/Spinner"


export default {
  data() {
    return {
      categories: [],
      filter: "",
      renderCategories: [],
      color: "#cdddf9",
      addPasswordModalVisible: false,
      editPasswordModalVisible: false,
      modalOpen: false,
      passwordKey: String,
      categoryRenderFlag: true,
      categoryMounted: false,
      zeroCategories: false
    };
  },
  components: {
    category: Category,
    navbar: Navbar,
    addPasswordModal: AddPasswordModal,
    editPasswordModal: EditPasswordModal,
    Spinner
  },
  methods: {
    fetchCategories() {
      var session = JSON.parse(window.sessionStorage.vuex);
      axios
        .post(BACKEND_URI + "/api/ListCategories", {
          session_key: session.session_key,
          user_key: session.user.user_key,
        })
        .then((response) => {
          this.categories = response.data.categories.sort((a, b) => {
            if (a.category_name < b.category_name) {
              return -1;
            }
            if (b.category_name < a.category_name) {
              return 1;
            }
            return 0;
          });
          this.renderCategories = this.categories;
          if (this.categories.length == 0) {
            this.zeroCategories = true;
            this.categoryMounted = true;
          } else {
            this.zeroCategories = false;
            this.categoryMounted = true;
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    openAddPasswordModal() {
      this.addPasswordModalVisible = true;
      this.openOverlay();
    },
    chooseColor() {
      var colors = ["#cdddf9", "#e6f2ff"];
      if (this.color == colors[0]) {
        this.color = colors[1];
      } else {
        this.color = colors[0];
      }
    },
    openOverlay() {
      this.modalOpen = true;
    },
    closeOverlay() {
      this.modalOpen = false;
    }
  },
  mounted() {
    this.fetchCategories();
    EventBus.$on("category-mounted", () => {
      this.categoryMounted = true;
    })
    EventBus.$on("close-delete-category-popup", () => {
      setTimeout(2000)
      this.fetchCategories();
      this.$forceUpdate();
    })
    EventBus.$on("close-add-password-modal",
      () => {
        this.fetchCategories();
        this.$forceUpdate(); 
        this.addPasswordModalVisible = false;
        this.closeOverlay();
      }
    );
    EventBus.$on("password-clicked",
      password => { 
        this.passwordKey = password.password_key;
        this.editPasswordModalVisible = true;
        this.openOverlay();
      }
    );
    EventBus.$on("close-edit-password-modal",
      () => {
        this.fetchCategories();
        this.$forceUpdate();
        this.editPasswordModalVisible = false;
        this.closeOverlay();
      }
    );
  },
  // watch: {
  //   filter: function () {
  //     if (this.filter == "") {
  //       this.renderCategories = this.categories;
  //     }
  //     if (this.filter != "") {
  //       var filterLength = this.filter.length;
  //       this.renderCategories = this.categories.filter((category) => {
  //         var catSub = category.category_name
  //           .toLowerCase()
  //           .substr(0, filterLength);
  //         return catSub == this.filter.toLowerCase();
  //       });
  //     }
  //   },
  // },
};
</script>

<style scoped>
@import "../../assets/scss/vault-view.scss";
</style>