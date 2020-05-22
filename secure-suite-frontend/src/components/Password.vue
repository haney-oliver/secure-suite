<template>
  <div class="password">
    <h3 v-on:click="openPasswordModal">{{ password.passwordCategory }}</h3>
    <h2 v-on:click="openPasswordModal">{{ password.passwordName }}</h2>
    <div class="ontop" id="overlay"></div>
    <passwordModal :password="password" v-if="isVisible" @closeModal="closePasswordModal" />
  </div>
</template>

<script>
import axios from "axios";
import PasswordModal from "@/components/PasswordModal";
export default {
  props: ["password"],
  data() {
    return {
      isVisible: false
    };
  },
  components: {
    passwordModal: PasswordModal
  },
  methods: {
    openPasswordModal: function() {
      this.isVisible = true;
      document.getElementById("overlay").style.visibility = "visible";
    },
    closePasswordModal: function() {
      this.isVisible = false;
      document.getElementById("overlay").style.visibility = "hidden";
    }
  },
  watch: {
    isVisible: function() {
      if (this.isVisible == false) {
        this.$emit("fetch");
      }
    }
  }
};
</script>

<style scoped>
.password {
  margin: 1em;
  display: inline-block;
  width: 100%;
  padding: 0;
  text-align: left;
  background-color: #ffffff;
  text-decoration: none;
  transition: color 0.15s ease, border-color 0.15s ease;
  max-width: 250px;
  border: 1px dotted #dfdfdf;
}

.password:hover,
.password:focus,
.password:active {
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  background-color: #fffbd6;
  -webkit-transition: background-color 300ms linear;
  -ms-transition: background-color 300ms linear;
  transition: background-color 300ms linear;
  cursor: pointer;
}

.password:hover h3 {
  color: #fffbd6;
  width: 100%;
}

.password h2 {
  margin: 0 0 1rem 0;
  text-align: center;
  font-size: 1.5rem;
  padding: 1em;
  padding-top: 0.25em;
  margin: 0;
}

.password h3 {
  color: white;
  margin: 0;
  font-size: 1.25rem;
  padding-left: 1em;
  padding-right: 1em;
  background-color: #2985ff;
  display: inline-block;
  overflow: hidden;
  width: 125px;
  transition: width 0.3s;
}
.xButton {
  margin: 1em;
  margin-top: 0;
  width: 20px;
  height: 20px;
  display: inline-block;
}

.ontop {
  visibility: hidden;
  z-index: 11;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  position: fixed;
  background-color: #19307c;
  opacity: 0.6;
}
</style>