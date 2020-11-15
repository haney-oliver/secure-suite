<template>
  <span class="vault">
    <div class="message">
      <h4 v-if="zeroCategories">You have no passwords. Click "Add New Password" above to get started.</h4>
    </div>
    <category
      v-for="category in categories"
      :key="category.category_key"
      v-bind:category="category"
      >
    </category>
  </span>
</template>

<script>
import axios from "axios";
import Category from "@/components/Category";
import { EventBus } from "@/event-bus";


export default {
  data() {
    return {
      categories: [],
      zeroCategories: false,
      passwordKey: String
    };
  },
  components: {
    Category
  },
  methods: {
    fetchCategories() {
      var session = JSON.parse(window.sessionStorage.vuex);
      axios
        .post("http://192.168.1.165:5000/api/ListCategories", {
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
          if (this.categories.length == 0) {
            this.zeroCategories = true;
          } else {
            this.zeroCategories = false;
          }
        })
        .catch((err) => {
          console.log(err);
        });
    }
  },
  mounted() {
    this.fetchCategories();
    EventBus.$on("password-clicked",
      password => { 
        this.passwordKey = password.password_key;
        this.openOverlay();
      }
    );
  }
};
</script>

<style scoped lang="scss">
@import url("https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;700&display=swap");

$font-stack: "Noto Sans", sans-serif;
$primary-color: rgb(0, 0, 0);
$button-color: #6480ff;
$button-hover: #4f6fff;

body {
    font: 100% $font-stack;
    color: $primary-color;
    background-color: white;
    width: 100%;
    margin: 0;
    padding: auto;

    h1 {
        font-size: xx-large;
    }

    h1.large-stat {
        font-size: 42px;
        margin: 0.25rem 0 0.25rem 0;
    }

    h2 {
        font-size: x-large;
        font: 100% $font-stack;
        display: inline;
        text-align: center;
    }
}

.container {
    margin: 1rem;
    text-align: center;
}

.input-field {
    width: 80%;
    margin: 1rem auto 1rem auto;
    height: 40px;
    font-size: 18px;
    padding: 0 0.5rem 0 0.5rem;
    display: block;
    text-align: center;
}

.form {
    width: 200px;
    margin: 1rem auto 1rem auto;
    position: relative;
    z-index: 5;
}

.danger {
    display: inline-block;
    border-radius: 4px;
    border: none;
    color: #ffffff;
    text-align: center;
    font-size: 20px;
    padding: 1rem;
    width: 50%;
    transition: all 0.5s;
    cursor: pointer;
    margin: 0.5rem;
    background-color: #ff6f6f
}

.danger:hover {
    background-color: #dd4949
}

.buttons {
    width: 100%;
    text-align: center;
    display: inline-block;

    .main-button {
        display: inline-block;
        border-radius: 4px;
        background-color: $button-color;
        border: none;
        color: #ffffff;
        text-align: center;
        font-size: 20px;
        padding: 1rem;
        width: 50%;
        transition: all 0.5s;
        cursor: pointer;
        margin: 0.5rem;
    }

    .main-button .button-content {
        cursor: pointer;
        display: inline-block;
        position: relative;
        transition: 0.5s;
    }

    .main-button .button-content:after {
        content: "\00bb";
        position: absolute;
        opacity: 0;
        top: 0;
        right: -20px;
        transition: 0.5s;
    }

    .main-button:hover .button-content {
        padding-right: 25px;
    }

    .main-button:hover .button-content:after {
        opacity: 1;
        right: 0;
    }

    .main-button:hover {
        background-color: $button-hover;
    }
}

.success-button {
    display: inline-block;
    border-radius: 4px;
    background-color: #9cf1bf;
    border: none;
    color: #058800;
    text-align: center;
    font-size: 20px;
    padding: 1rem;
    width: 50%;
    transition: all 0.5s;
    cursor: pointer;
    margin: 0.5rem;
}

.success-button .button-content {
    cursor: pointer;
    display: inline-block;
    position: relative;
    transition: 0.5s;
}

.success-button:hover {
    cursor: default;
}

.success-button .button-content:after {
    content: "\00bb";
    position: absolute;
    opacity: 0;
    top: 0;
    right: -20px;
    transition: 0.5s;
}

.success-button:hover .button-content {
    padding-right: 25px;
}

footer {
    margin: 8rem auto 8rem auto;
    display: block;
    text-align: center;
}

a {
    text-decoration: none;
    color: $button-color;
}

a:hover {
    color: $button-hover;
}

#searchContainer {
    background-color:rgb(205, 221, 249);
    height: 80px;
    margin-top: 0;
    padding-top: 1rem;
}

#searchField {
    width: 70%;
    margin: 1rem auto 1rem auto;
    display: block;
}

.vault {
    background-color: "#cdddf9";
    .container{
        margin: 0;
    }
    .spacer {
        height: 50px;
        width: 100%;
    }
    width: 95%;
    margin: 1rem auto 1rem auto;
    position: relative;
    z-index: 5;
}

.message {
    display: inline;
    text-align: center;
}

.vault-buttons {
    width: 100%;
    text-align: center;
    display: inline-block;
    background-color:rgb(205, 221, 249);
}

.modalopen {
    position: fixed;
    height: 100%;
    width: 100%;
    background-color: rgba(0, 0, 0, 0.514);
    filter: blur(2px); -webkit-filter: blur(2px);
}

.refresh-icon {
    position: relative;
    z-index: 21;
    height: 30px;
    width: 30px;
    cursor: pointer;
}
</style>