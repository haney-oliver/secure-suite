<template>
  <router-view />
</template>

<script>
import router from "@/router/index";
export default {
  mounted() {
    if (navigator.storage && navigator.storage.persist)
      navigator.storage.persist().then(function (persistent) {
        if (persistent)
          console.log(
            "Storage will not be cleared except by explicit user action"
          );
        else
          console.log(
            "Storage may be cleared by the UA under storage pressure."
          );
      });
    let user;
    let session_key;
    browser.storage.local.get("user").then((obj) => {
      user = obj.user;
      console.log(obj)
      browser.storage.local.get("session_key").then((obj) => {
        session_key = obj.session_key;
        console.log("App: ", user, session_key);
        if (!user || !session_key) {
          router.replace("/login");
        } else {
          router.replace("/vault");
        }
      });
    });
  },
};
</script>

<style>
html {
  width: 400px;
  height: 500px;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: #6480ff #ebebeb;
}

body {
  width: 400px;
  overflow-x: hidden;
}
</style>
