<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "App",
  methods: {
    logout() {
      axios
        .post("http://localhost:8080/api/DeleteSession", {
          sessionId: this.getCookie("ssid")
        })
        .then(response => {
          var code = response.data.status;
          if (code == 200) {
            document.cookie = "ssid=";
            document.location.href = "/";
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
    createSession() {
      if (this.getCookie("ssid") == "") {
        axios
          .post("http://localhost:8080/api/CreateSession")
          .then(response => {
            var code = response.data.status;
            if (code == 200) {
              document.cookie = "ssid=" + response.data.sessionId;
            } else {
              console.log(
                "Status: " +
                  code +
                  " ErrorMessage: " +
                  response.data.errorMessage
              );
            }
          })
          .catch(error => {
            console.log(error);
          });
      }
    }
  },
  created() {
    this.createSession();
  },
  beforeDestroy() {
    this.logout();
  }
};
</script>

<style>
html,
body {
  padding: 0;
  margin: 0;
  font-family: "Nunito";
}

* {
  box-sizing: border-box;
}

main h1 {
  padding-top: 80px;
}

footer {
  padding-top: 70px;
  padding-bottom: 100px;
  margin-top: 2.5em;
  margin-bottom: 1.5em;
  text-align: center;
}

.container {
  width: 70%;
  height: auto;
  margin-left: auto;
  margin-right: auto;
  text-align: center;
}

.container h2 {
  margin-top: 3em;
  margin-bottom: 0.5em;
}

.banner {
  width: 100%;
  height: 500px;
  align-items: center;
  padding-bottom: 0;
  padding-top: 1em;
  padding-left: 1em;
  padding-right: 1em;
  background-image: url("./assets/images/secrets-manager-banner.svg"),
    linear-gradient(0deg, rgb(218, 241, 255) 0%, rgb(125, 173, 255) 100%);
  background-size: contain;
  background-position: center;
  position: relative;
  background-repeat: no-repeat;
}

.banner .bannerTitle {
  float: left;
  display: block;
  padding-left: 6rem;
  width: 59%;
  height: 30%;
}

.banner h1 {
  text-align: center;
  font-size: 4.5rem;
  color: white;
  margin-bottom: 0;
  margin-top: 0;
  padding-left: 0;
  padding-right: 0;
  z-index: 10;
}

.banner h1:hover,
.banner h1:active,
.banner h1:focus {
  color: #faf4be;
}

.banner h2 {
  text-align: center;
  font-size: 1.5rem;
  color: black;
  margin-top: 0;
  margin-bottom: 2em;
  padding-left: 0;
  padding-right: 5px;
  display: block;
  float: right;
}

.banner h2:hover,
.banner h2:active,
.banner h2:focus {
  color: #faf4be;
}

.navbar {
  padding-top: 5px;
  height: 50px;
  width: 100%;
  padding-bottom: 3.5em;
  background-color: rgb(218, 241, 255);
  border-bottom: 1px solid hsl(231, 24%, 40%);
  margin-bottom: 1em;
  margin-top: 0;
  z-index: 100;
}

.navbar ul {
  float: right;
  list-style-type: none;
  display: block;
  padding-right: 30px;
  padding-bottom: 3em;
}

.navbar ul.smi {
  float: left;
}

.navbar li {
  display: inline-block;
  text-align: center;
  vertical-align: middle;
  border: thick;
  border-color: black;
  margin-right: 10px;
}

main {
  padding: 5rem 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

a {
  color: inherit;
  text-decoration: none;
}

a:hover {
  color: #0f77ff;
  border: 1px;
}

.title a {
  color: #59f3d2;
  text-decoration: none;
}

.title a:hover,
.title a:focus,
.title a:active {
  text-decoration: underline;
}

.title {
  margin: 0;
  line-height: 1.15;
  font-size: 4rem;
}

.title,
.description {
  text-align: center;
}

.description {
  line-height: 1.5;
  font-size: 1.5rem;
}

code {
  background: #fafafa;
  border-radius: 5px;
  padding: 0.75rem;
  font-size: 1.1rem;
  font-family: Menlo, Monaco, Lucida Console, Liberation Mono, DejaVu Sans Mono,
    Bitstream Vera Sans Mono, Courier New, monospace;
}

.grid {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  max-width: 1000px;
  margin-top: 3rem;
  width: 100%;
  flex-direction: row;
  margin-left: auto;
  margin-right: auto;
}

.grid .articlePicture {
  max-width: 450px;
  max-height: 450px;
  margin: 0.5em;
}

.grid .articleParagraph {
  margin: 0.5em;
  flex-basis: 45%;
  padding: 1.5rem;
  text-align: center;
  color: inherit;
  text-decoration: none;
  transition: color 0.15s ease, border-color 0.15s ease;
  max-width: 380px;
}

.card {
  margin: 1rem;
  flex-basis: 45%;
  padding: 1.5rem;
  text-align: left;
  color: inherit;
  text-decoration: none;
  border: 1px solid #eaeaea;
  border-radius: 10px;
  transition: color 0.15s ease, border-color 0.15s ease;
}

.card:hover,
.card:focus,
.card:active {
  color: #faf4be;
  border-color: #faf4be;
}

.card h3 {
  margin: 0 0 1rem 0;
  font-size: 1.5rem;
}

.card p {
  margin: 0;
  font-size: 1.25rem;
  line-height: 1.5;
}

article {
  margin: 1rem;
  flex-basis: 45%;
  padding: 1.5rem;
  text-align: center;
  color: inherit;
  text-decoration: none;
  border: 1px solid #eaeaea;
  border-radius: 10px;
  transition: color 0.15s ease, border-color 0.15s ease;
  max-width: 365px;
  min-height: 320px;
  min-width: 260px;
}

article:hover,
article:focus,
article:active {
  color: #000000;
  border-color: #000000;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
}

article h3 {
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 0;
  font-size: 1.5rem;
}

article p {
  margin-left: auto;
  margin-right: auto;
  margin-bottom: auto;
  margin-top: 0;
  font-size: 1.25rem;
  line-height: 1.5;
}

article img {
  width: 80%;
  height: 120px;
  display: block;
  padding: auto auto auto auto;
  margin-left: auto;
  margin-right: auto;
  margin-top: auto;
  margin-bottom: 1em;
}

.sticky {
  position: fixed;
  top: 0;
  margin-top: 0;
  padding-bottom: 3.5em;
  height: 50px;
  background-color: #2985ff;
  -webkit-transition: background-color 200ms linear;
  -ms-transition: background-color 200ms linear;
  transition: background-color 200ms linear;
}

.sticky + .container {
  padding-top: 58px;
}

.sticky a {
  color: white;
}

.sticky a:hover {
  color: rgb(255, 238, 0);
}

.form {
  display: block;
  width: 50%;
  margin-right: auto;
  margin-left: auto;
  text-align: center;
}

.form .formTitle {
  text-align: center;
  font-size: 2.5rem;
}

.inputField {
  text-align: center;
  padding-bottom: 0.5em;
  padding-top: 0.5em;
  margin-bottom: 1em;
  width: 100%;
  font-size: 1.5rem;
}

#searchButton {
  display: block;
  max-width: 100px;
  float: right;
}

#searchField {
  display: block;
  float: left;
  width: 100%;
}

button {
  margin-left: auto;
  margin-right: auto;
  padding-top: 0.5em;
  padding-bottom: 0.5em;
  background-color: white;
  color: #2985ff;
  border: none;
  width: 40%;
  font-size: 1.5rem;
}

button:hover,
button:active,
button:focus {
  cursor: pointer;
  background-color: #2985ff;
  color: white;
  -webkit-transition: background-color 200ms linear;
  -ms-transition: background-color 200ms linear;
  transition: background-color 200ms linear;
}

.form button {
  display: inline;
  margin: 0.5em;
}

.slidecontainer {
  width: 100%;
  outline: none;
}

.slider {
  -webkit-appearance: none;
  width: 100%;
  height: 15px;
  background: #d3d3d3;
  opacity: 0.5;
  -webkit-transition: 0.2s;
  transition: opacity 0.2s;
  margin-bottom: 0.5em;
  outline: none;
}

.slider:active,
.slider:focus {
  outline: none;
}

.slider:hover {
  opacity: 1;
  outline: none;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 15px;
  height: 15px;
  background: #2985ff;
  cursor: pointer;
  outline: none;
}

.slider::-moz-range-thumb {
  width: 25px;
  height: 25px;
  background: #2985ff;
  cursor: pointer;
  outline: none;
}

.xButton {
  width: 35px;
  height: 35px;
  background: url("./assets/images/x-button.svg");
  background-repeat: no-repeat;
  background-position: center;
  background-size: 100%;
  float: right;
  display: block;
  position: relative;
}

.xButton:active,
.xButton:hover,
.xButton:focus {
  cursor: pointer;
  background: url("./assets/images/x-button-active.svg");
  background-repeat: no-repeat;
  background-position: center;
  background-size: 100%;
}

@media (max-width: 1000px) {
  .grid {
    width: 100%;
  }
  .container {
    width: 80%;
  }

  article {
    width: 100%;
  }
}

@media (max-width: 800px) {
  .navbar ul {
    float: none;
    display: inline;
    padding-right: 0;
    padding-left: 0;
  }

  .navbar {
    text-align: center;
    padding-bottom: 3em;
    padding-top: 1em;
  }
}

@media (max-width: 600px) {
  .grid {
    flex-direction: column;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-2em);
  }

  to {
    opacity: 1;
    transform: translateY(-2em);
  }
}
</style>
