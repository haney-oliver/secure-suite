<template>
  <div id="vault">
    <div class="navbar" id="navbar">
      <ul class="option">
        <li>
          <router-link
            :to="{name: 'Dashboard', params: { userId: this.$route.params.userId}}"
          >Dashboard</router-link>
        </li>
        <li>
          <router-link to="/preferences">Preferences</router-link>
        </li>
        <li>
          <a v-on:click="logout">Logout</a>
        </li>
      </ul>
    </div>
    <div class="container">
      <h1>VAULT</h1>
      <div id="searchContainer">
        <input
          type="text"
          class="inputField"
          id="searchField"
          placeholder="Filter by category"
          v-model="filter"
        />
      </div>
      <div>
        <button id="addPassword" v-on:click="openModal">Add New Password</button>
      </div>
      <div class="grid" id="vaultGrid">
        <password
          v-for="password in renderPasswords"
          v-bind:key="password.passwordId"
          :password="password"
          @fetch="getPasswords()"
        />
      </div>
    </div>
    <div class="ontop" id="overlay"></div>
    <addPasswordModal v-if="isVisible" @close="closeModal" />
  </div>
</template>

<script>
import axios from "axios";
import Password from "@/components/Password";
import AddPasswordModal from "@/components/AddPasswordModal";

export default {
  name: "vault",
  components: {
    addPasswordModal: AddPasswordModal,
    password: Password
  },
  props: ["userId"],
  data() {
    return {
      filter: "",
      renderPasswords: [],
      passwords: [],
      isVisible: false
    };
  },
  methods: {
    getPasswords() {
      axios
        .post("http://localhost:8080/api/ListPassword", {
          refUserId: this.$route.params.userId
        })
        .then(response => {
          var code = response.data.status;
          if (code == 200) {
            this.passwords = response.data.passwords.sort((a, b) => {
              if (a.passwordCategory < b.passwordCategory) {
                return -1;
              }
              if (b.passwordCategory < a.passwordCategory) {
                return 1;
              }

              if (a.passwordName < b.passwordName) {
                return -1;
              }

              if (b.passwordName < a.passwordName) {
                return 1;
              }
              return 0;
            });
            this.renderPasswords = this.passwords;
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
    openModal() {
      this.isVisible = true;
      document.getElementById("overlay").style.visibility = "visible";
    },
    closeModal() {
      this.isVisible = false;
      document.getElementById("overlay").style.visibility = "hidden";
    },
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
    logout() {
      var ssid = this.getCookie("ssid");
      axios
        .post("http://localhost:8080/api/LogoutUser", {
          userId: this.$route.params.userId
        })
        .then(response => {
          var code = response.data.status;
          if (code == 200) {
            axios
              .post("http://localhost:8080/api/DeleteSession", {
                sessionId: ssid
              })
              .then(function(response) {
                var code = response.data.status;
                if (code == 200) {
                  document.cookie = "ssid=";
                  document.location.href = "/";
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
          }
        })
        .catch(error => {
          console.log(error);
        });
    }
  },
  created() {
    this.getPasswords();
  },
  mounted() {
    window.onscroll = function() {
      myFunction();
    };

    var navbar = document.getElementById("navbar");

    var sticky = navbar.offsetTop;

    function myFunction() {
      if (window.pageYOffset >= sticky) {
        navbar.classList.add("sticky");
      } else {
        navbar.classList.remove("sticky");
      }
    }
  },
  watch: {
    filter: function() {
      if (this.filter == "") {
        this.renderPasswords = this.passwords;
      }
      if (this.filter != "") {
        var filterLength = this.filter.length;
        this.renderPasswords = this.passwords.filter(password => {
          var catSub = password.passwordCategory.substr(0, filterLength);
          return catSub == this.filter;
        });
      }
    },
    isVisible: function() {
      if (this.isVisible == false) {
        this.getPasswords();
      }
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

#addPassword {
  max-width: 250px;
  margin-top: 1em;
}

#vault {
  background-color: #ffffff;
  padding-bottom: 5rem;
}

#vault h1 {
  font-size: 5rem;
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

a:hover {
  cursor: pointer;
}
</style>