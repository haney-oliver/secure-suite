<template>
  <div>
    <navbar />
    <div class="container">
      <div class="form">
        <div class="form-content">
          <span class="buttons">
            <button class="main-button">Update Username</button>
            <button class="main-button">Update Password</button>
            <button class="main-button">Update Email</button>
            <button class="danger">Delete Account</button>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from "@/components/Navbar"
import { EventBus } from "@/event-bus"


export default {
  components: {
    Navbar
  },
  data() {
    return {
      updateUsernamePopupVisible: false,
      updatePasswordPopupVisible: false,
      updateEmailPopupVisible: false,
      deleteAccountPopupVisible: false,
    }
  },
  methods: {
    updateUsername() {},
    updatePassword() {},
    updateEmail() {},
    deleteAccount() {},
    openUpdateUsernamePopup() {
      this.updateUsernamePopupVisible = true;
    },
    openUpdatePasswordPopup() {
      this.updatePasswordPopupVisible = true;
    },
    openUpdateEmailPopup() {
      this.updateEmailPopupVisible = true;
    },
    openDelteAccountPopup() {
      this.deleteAccountPopupVisible = true;
    }
  },
  mounted() {
    EventBus.$on("close-update-username-popup", () => {
      this.updateUsernamePopupVisible = false;
    })
    EventBus.$on("close-update-password-popup", () => {
      this.updateUsernamePopupVisible = false;
    })
    EventBus.$on("close-update-email-popup", () => {
      this.updateUsernamePopupVisible = false;
    })
    EventBus.$on("close-delete-account-popup", () => {
      this.updateUsernamePopupVisible = false;
    })
  }
}
</script>

<style scoped>
@import "../../assets/scss/preferences-view.scss";
</style>