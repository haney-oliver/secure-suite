<template>
  <span class="password" @click.self="emitPassword">
    <div class="icon-input-field">
      <h3 class="password-url">{{ password.password_url }}</h3>
      <div
        :class="{'passwordFieldIcon': !passwordCopied, 'checkmark-icon': passwordCopied}"
        v-on:click="copyToClipboard"
      ></div>
    </div>
  </span>
</template>

<script>
import { EventBus } from "@/event-bus";
export default {
  props: {
    password: Object,
  },
  data() {
    return {
      passwordCopied: false
    }
  },
  methods: {
    emitPassword() {
      EventBus.$emit("password-clicked", this.password);
    },
    copyToClipboard() {
        navigator.clipboard.writeText(this.password.password_content);
        this.passwordCopied = true;
    }
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
  width: 100%;
  margin: 0;
  overflow: auto;
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

.password {
  display: inline-block;
  padding: 0.5rem 0.5rem 1rem 0.5rem;
  margin: 0;
  background-color: white;
  height: 30px;
  width: 95%;
  font: 100% $font-stack;
  border-bottom: 1px solid #4b9efd;
  cursor: pointer;
}
.password-url {
  display: block;
  float: left;
  margin: 0 1rem 0 0.5rem;
  font: 100% $font-stack;
}

.icon-input-field {
  display: block;
  width: 100%;
  padding: 0.5rem;
  text-align: center;
}

.passwordFieldIcon {
    display: block;
    border: none;
    width: 22px;
    height: 22px;
    background-image: url("../assets/copy-icon.svg");
    background-repeat: no-repeat;
    background-position: center;
    background-size: 100%;
    margin: 0rem 0.25rem 0.5rem 0.25rem;
    float: right;
}

.passwordFieldIcon:hover {
    background-image: url("../assets/copy-icon-active.svg");
    background-repeat: no-repeat;
    background-position: center;
    background-size: 100%;
    cursor: pointer;
}

.checkmark-icon {
    display: block;
    border: none;
    width: 22px;
    height: 22px;
    background-image: url("../assets/checkmark.svg");
    background-repeat: no-repeat;
    background-position: center;
    background-size: 100%;
    margin: 0rem 0.25rem 0.5rem 0.25rem;
    float: right;
}
</style>