<template>
  <span v-if="showCat" class="category">  
    <h3 class="category-name">{{ category.category_name }}</h3>
    <password
      v-for="password in passwords"
      :key="password.password_key"
      v-bind:password="password"
    />
  </span>
</template>

<script>
import axios from "axios";
import Password from "@/components/Password";
import { EventBus } from '@/event-bus';

export default {
  props: {
    category: Object,
    color: String
  },
  data() {
    return {
      passwords: [],
      showCat: false,
      user: Object,
      session_key: String
    };
  },
  components: {
    password: Password
  },
  methods: {
    fetchPasswords() {
      axios
        .post("http://192.168.1.165:5000/api/ListPasswords", {
          session_key: this.session_key,
          user_key: this.user.user_key,
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
    }
  },
  mounted() {
    browser.storage.local.get("user").then((obj) => {
      this.user = JSON.parse(obj.user);
      console.log(this.user);
      browser.storage.local.get("session_key").then((obj) => {
        this.session_key = obj.session_key;
        console.log(this.session_key);
        this.fetchPasswords();
      });
    });
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
    font: 100% $font-stack;
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

.category {
    padding: 0;
    display: block;
    text-align: center;
    width: 100%;
    margin: 0 auto 0 auto;
}

.category-name {
    display: block;
    text-align: center;
    margin: 0;
    font: 100% $font-stack;
    color: #ffffff;
    background-color: #6480ff;
    width: 100%;
}



.fade-enter-active, .fade-leave-active {
    transition: opacity .5s;
}

.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
    opacity: 0;
}

</style>