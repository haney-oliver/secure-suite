<template>
  <div class="navbar">
    <span class="title">SECURE SUITE</span>
    <ul class="options">
      <li>
        <a href="http://192.168.1.165:8080/">Home</a>
      </li>
      <li v-if="user">
        <a class="alternative" @click="logOut">Logout</a>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import { EventBus } from "@/event-bus";
import axios from "axios";
import store from "@/store";
import router from "@/router/index";

export default {
  name: "Navbar",
  data() {
    return {
      showList: false,
      user: Object,
      session_key: String,
    };
  },
  methods: {
    logOut() {
      axios
        .post("http://192.168.1.165:5000/api/LogoutUser", {
          user_key: this.user.user_key,
          session_key: this.session_key,
        })
        .then(() => {
          browser.storage.local.clear().then(() => {
            console.log("Logged out and cleared");
            store.dispatch("removeUserAndSession");
            router.replace("/login");
          });
        })
        .catch((response) => console.log(response.message));
    },
  },
  mounted() {
    browser.storage.local.get("user").then((obj) => {
      this.user = JSON.parse(obj.user);
      console.log(this.user);
      browser.storage.local.get("session_key").then((obj) => {
        this.session_key = obj.session_key;
        console.log(this.session_key);
      });
    });
  },
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
  background-color: #ff6f6f;
}

.danger:hover {
  background-color: #dd4949;
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

.navbar {
  height: 65px;
  width: 100%;
  background-color: #6480ff;
  margin: 0;
  z-index: 100;
  font: 100% $font-stack;
  margin-bottom: 0.25rem;

  .title {
    display: block;
    float: left;
    margin: 1.35rem 0 0 1rem;
    font-weight: 700;
    color: #c2c3ff;
    font: 100% $font-stack;
  }

  .options {
    float: right;
    list-style-type: none;
    display: block;
    padding: 0 1rem 0 0;
    margin-top: 1.25rem;
    font: 100% $font-stack;

    li {
      display: inline-block;
      font-size: 14px;

      a {
        cursor: pointer;
        text-decoration: none;
        color: rgb(255, 255, 255);
        padding: 1rem;
        font: 100% $font-stack;
      }

      a:hover {
        background-color: #4f6fff;
        transition: 0.5s;
      }

      .alternative:hover {
        color: #4f6fff;
        background-color: #ffffff;
        transition: 0.5s;
      }
    }
  }
}
</style>
