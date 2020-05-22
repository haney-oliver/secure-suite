<template>
  <div class="login">
    <div class="navbar" id="navbar">
      <ul class="option">
        <li>
          <router-link to="/">Home</router-link>
        </li>
        <li>
          <router-link to="/register">Register</router-link>
        </li>
      </ul>
    </div>

    <div class="form" id="loginForm">
      <h2 class="formTitle">Login</h2>
      <input class="inputField" type="text" id="usernameInput" placeholder="Username" />
      <input class="inputField" type="password" id="passwordInput" placeholder="Password" />
      <button v-on:click="submitLoginForm" id="loginButton">Login</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "login",
  methods: {
    getCookie(cname) {
      var name = cname + "=";
      var decodedCookie = decodeURIComponent(document.cookie);
      var ca = decodedCookie.split(";");
      for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == " ") {
          c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
          return c.substring(name.length, c.length);
        }
      }
      return "";
    },
    submitLoginForm: function() {
      var username = document.getElementById("usernameInput").value;
      var password = document.getElementById("passwordInput").value;
      var ssid = this.getCookie("ssid");
      console.log(username + " " + password);
      axios
        .post("http://localhost:8080/api/LoginUser", {
          userName: username,
          userPassword: password,
          sessionId: ssid
        })
        .then(function(response) {
          var code = response.data.status;
          var user;
          if (code == 200) {
            user = response.data.user;
            axios
              .post("http://localhost:8080/api/UpdateSession", {
                session: {
                  sessionId: ssid,
                  refUserId: user.userId,
                  loginAttempts: 1,
                  loggedIn: true
                }
              })
              .then(function(response) {
                var code = response.data.status;
                if (code == 200) {
                  window.location = "/#/vault/" + user.userId;
                } else {
                  console.log(
                    "Status: " +
                      code +
                      " ErrorMessage: " +
                      response.data.errorMessage
                  );
                }
              })
              .catch(function(error) {
                console.log(error);
              });
          } else {
            console.log(
              "Status: " + code + " ErrorMessage: " + response.data.errorMessage
            );
            // axios
            //   .post("http://localhost:8080/api/UpdateSession", {
            //     session: {
            //       sessionId: this.getCookie('ssid'),
            //       refUserId: "guest",
            //       loginAttempts: 1,
            //       loggedIn: false
            //     }
            //   })
            //   .then(function(response) {
            //     var code = response.data.status;
            //     if (code == 200) {
            //       window.location = "/#/vault/" + user.userId;
            //     } else {
            //       console.log(
            //         "Status: " +
            //           code +
            //           " ErrorMessage: " +
            //           response.data.errorMessage
            //       );
            //     }
            //   })
            //   .catch(function(error) {
            //     console.log(error);
            //   });
          }
        })
        .catch(function(error) {
          console.log(error);
        });
    }
  }
};
</script>

<style scoped>
.navbar {
  background-color: #2985ff;
}

.navbar a {
  color: white;
}

.navbar a:hover,
.navbar a:active,
.navbar a:focus {
  color: rgb(255, 238, 0);
}
</style>