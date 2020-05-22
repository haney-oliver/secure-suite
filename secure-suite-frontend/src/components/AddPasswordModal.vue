<template>
  <div id="addPasswordModal">
    <div class="xButton" v-on:click="closePasswordModal"></div>
    <div class="form" id="addPasswordModalForm">
      <h2 class="formTitle">Add Password</h2>
      <input class="inputField" type="text" id="passwordNameInput" placeholder="Password Name" />
      <div class="iconSearchField">
        <input
          class="inputField"
          type="password"
          id="passwordContentInput"
          placeholder="Password Content"
        />
        <div class="searchFieldIcon" v-on:click="togglePasswordVisibility"></div>
      </div>
      <input
        class="inputField"
        type="text"
        id="passwordUsernameInput"
        placeholder="Password Username"
      />
      <input
        class="inputField"
        type="text"
        id="passwordCategoryInput"
        placeholder="Password Category"
      />
      <input class="inputField" type="text" id="passwordUrlInput" placeholder="Password Url" />
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
      <button v-on:click="generatePassword" id="generatePasswordButton">Generate</button>
      <button v-on:click="submitPasswordForm" id="submitPasswordForm">Add</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      length: 25
    };
  },
  methods: {
    generatePassword() {
      var length = this.length;
      var passwordField = document.getElementById("passwordContentInput");
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
    submitPasswordForm() {
      axios
        .post("http://localhost:8080/api/CreatePassword", {
          refUserId: this.$route.params.userId,
          password: {
            refUserId: this.$route.params.userId,
            passwordName: document.getElementById("passwordNameInput").value,
            passwordContent: document.getElementById("passwordContentInput")
              .value,
            passwordUsername: document.getElementById("passwordUsernameInput")
              .value,
            passwordUrl: document.getElementById("passwordUrlInput").value,
            passwordCategory: document.getElementById("passwordCategoryInput")
              .value
          }
        })
        .then(response => {
          var code = response.data.status;
          if (code == 200) {
            this.closePasswordModal();
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
    togglePasswordVisibility() {
      var x = document.getElementById("passwordContentInput");
      if (x.type === "password") {
        x.type = "text";
      } else {
        x.type = "password";
      }
    },
    closePasswordModal() {
      this.$emit("close");
    }
  },
  watch: {
    length: function() {
      this.generatePassword();
    }
  }
};
</script>

<style scoped>
#addPasswordModal {
  padding: 1em;
  position: fixed;
  margin: 5% auto; /* Will not center vertically and won't work in IE6/7. */
  left: 0;
  right: 0;
  bottom: 4em;
  background-color: white;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  width: 60%;
  z-index: 20; 
}

.xButton {
  margin-top: 2em;
  margin-right: 2em;
}

.inputField {
  padding-top: 0.25em;
  padding-bottom: 0.25em;
}

.iconSearchField {
  display: inline-block;
  border: 1px solid #ccc;
  margin-bottom: 1.5em;
  width: 100%;
  padding: 0.5em;
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