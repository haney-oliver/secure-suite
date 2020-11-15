<template>
  <div class="form" id="loginForm">
    <h2 class="form-title">Login</h2>
    <input
      class="input-field"
      type="text"
      v-model="username"
      placeholder="Username"
    />
    <input
      class="input-field"
      type="password"
      v-model="userPassword"
      placeholder="Password"
    />
    <span class="buttons">
      <button class="main-button" v-on:click="login" id="loginButton">
        <span class="button-content">Login</span>
      </button>
    </span>
  </div>
</template>

<script>
import axios from "axios";
import store from "@/store";
import router from "@/router/index";
import { EventBus } from "@/event-bus";

export default {
  name: 'Login',
  data() {
    return {
      username: "",
      userPassword: ""
    };
  },
  methods: {
    login() {
      axios
        .post("http://192.168.1.165:5000/api/LoginUser", {
          user_name: this.username,
          user_password: this.userPassword
        })
        .then(response => {
          var data = {
            user: response.data.user,
            session_key: response.data.session.session_key
          };
          store.dispatch("setUserAndSession", data).catch(error => console.log(error));
          router.replace("/vault");
          browser.runtime.sendMessage({type: "notification", options: {
            type: "basic",
            message: {user: data.user, session_key: data.session_key}
          }})
        })
        .catch(error => console.log(error));
    }
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
    width: 95%;
    margin: 1rem auto 1rem auto;
    height: 25px;
    font-size: 12px;
    padding: 0 0.5rem 0 0.5rem;
    display: block;
    text-align: center;
}

.form {
    width: 90%;
    margin: 1rem auto 1rem auto;
    position: relative;
    z-index: 5;
}

h2 {
      display: inline;
      text-align: center;
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

.login-view {
  .form {
    margin-top: 5rem;
  }
}
</style>
