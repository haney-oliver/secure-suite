<template>
  <div class="passwordModal">
    <div class="xButton" v-on:click="closePasswordModal"></div>
    <div class="form">
      <h1>{{ password.passwordName }}</h1>
      <input
        type="text"
        class="inputField"
        v-model="password.passwordCategory"
        :id="'passwordCategory' + password.passwordId"
        placeholder="Password Category"
      />
      <input
        type="text"
        class="inputField"
        v-model="password.passwordName"
        :id="'passwordName' + password.passwordId"
        placeholder="Password Name"
      />
      <div class="iconSearchField">
        <input
          class="inputField"
          type="password"
          placeholder="Password Content"
          v-model="password.passwordContent"
          :id="'passwordContent' + password.passwordId"
        />
        <div class="searchFieldIcon" v-on:click="togglePasswordVisibility(password.passwordId)"></div>
      </div>
      <input
        type="text"
        class="inputField"
        v-model="password.passwordUsername"
        :id="'passwordUsername' + password.passwordId"
        placeholder="Password Username"
      />
      <input
        type="text"
        class="inputField"
        v-model="password.passwordUrl"
        :id="'passwordUrl' + password.passwordId"
        placeholder="Password Url"
      />
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
      <button v-on:click="generatePassword(password.passwordId)" id="generatePasswordButton">Generate</button>
      <button v-on:click="updatePassword(password.passwordId)">Save</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: ["password"],
  data() {
    return {
      isVisible: false,
      length: 25
    };
  },
  created() {
    this.$on("closeModal", isVisible => {
      this.isVisible = isVisible;
    });
  },
  methods: {
    generatePassword(passwordId) {
      var length = this.length;
      var passwordField = document.getElementById("passwordContent" + passwordId);
      axios
        .post("http://localhost:8080/api/GeneratePassword", {
          length: length
        })
        .then(response => {
          var code = response.data.status;
          if (code == 200) {
            passwordField.value = response.data.generatedPassword;
          } else {
            console.log(
              "Status: " + code + " ErrorMessage: " + response.data.errorMessage
            );
          }
        })
        .catch(error => {
          console.log(error);
        });
    },
    togglePasswordVisibility(passwordId) {
      var x = document.getElementById("passwordContent" + passwordId);
      if (x.type === "password") {
        x.type = "text";
      } else {
        x.type = "password";
      }
    },
    updatePassword(passwordId) {
      axios
        .post("http://localhost:8080/api/UpdatePassword", {
          refUserId: this.$route.params.userId,
          password: {
            passwordId: passwordId,
            refUserId: this.$route.params.userId,
            passwordName: document.getElementById("passwordName" + passwordId)
              .value,
            passwordContent: document.getElementById(
              "passwordContent" + passwordId
            ).value,
            passwordUsername: document.getElementById(
              "passwordUsername" + passwordId
            ).value,
            passwordUrl: document.getElementById("passwordUrl" + passwordId)
              .value,
            passwordCategory: document.getElementById(
              "passwordCategory" + passwordId
            ).value
          }
        })
        .then(response => {
          var code = response.data.status;
          if (code == 200) {
              this.closePasswordModal()
          } else {
            console.log(
              "Status: " + code + " ErrorMessage: " + response.data.errorMessage
            );
          }
        })
        .catch(error => {
          console.log(error);
        });
    },
    closePasswordModal: function() {
      this.$emit("closeModal");
    }
  },
  watch: {
    length: function() {
      this.generatePassword(this.password.passwordId);
    }
  }
};
</script>

<style scoped>
.xButton {
  margin-right: 2em;
}

.inputField {
  padding-top: 0.25em;
  padding-bottom: 0.15em;
}

.iconSearchField {
  display: inline-block;
  border: 1px solid #ccc;
  margin-bottom: 1.5em;
  width: 100%;
  padding: 0.5em;
  background-color: white;
}

.iconSearchField .inputField {
  border: none;
  padding: 0;
  display: inline-block;
  margin-bottom: 0;
  width: 75%;
  vertical-align: middle;
}

.iconSearchField .searchFieldIcon {
  display: inline-block;
  border: none;
  width: 30px;
  height: 30px;
  background-image: url("../assets/images/visibility.svg");
  background-repeat: no-repeat;
  background-position: center;
  background-size: 100%;
  vertical-align: middle;
}

.iconSearchField .searchFieldIcon:hover {
  background-image: url("../assets/images/visibility-active.svg");
  background-repeat: no-repeat;
  background-position: center;
  background-size: 100%;
  cursor: pointer;
}

.passwordModal {
  padding: 1em;
  position: fixed;
  margin: 5% auto; /* Will not center vertically and won't work in IE6/7. */
  left: 0;
  right: 0;
  bottom: 5em;
  background-color: white;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  width: 60%;
  z-index: 20;
}

.xButton {
  margin: 1.5em;
}

button {
  display: inline;
}

.form {
  width: 60%;
}

.form h2 {
  margin: 1em;
}

@media (max-width: 800px) {
  .form {
      width: 85%;
  }
}
</style>