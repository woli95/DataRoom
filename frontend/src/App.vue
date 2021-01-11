<!--TODO:-->
<!--1. RESET PASSWORD MAIL NIE DZIAŁA -->



<template>
  <AuthView v-if="session_token === null" />
  <AppView v-if="session_token !== null" />
</template>

<script>
import AuthView from "@/components/AuthView.vue";
import AppView from "@/components/AppView";
import axios from "axios";


export default {
  name: 'App',
  computed: {
    console: () => console
  },
  components: {
    AppView,
    AuthView,
  },
  methods: {
    async registerUser(email, password) {
      let result = [false, ''];
      await axios.post(this.backend_url.concat('/client/create'), {
        email: email,
        password: password
      }).then((response) => {
        if (response.status === 200)
          result[0] = true;
        result[1] = response.data;
      }).catch((error) => {
        result[1] = error.message;
      });
      return result;
    },
    async loginUser(email, password) {
      let result = [false, ''];
      await axios.post(this.backend_url.concat('/client/login'), {
        email: email,
        password: password
      }).then((response) => {
        if (response.status === 200)
          result[0] = true;
        result[1] = response.data;
      }).catch((error) => {
        result[1] = error.message;
      });
      return result;
    },
    async changeUserEmail(new_email) {
      let result = [false, ''];
      await axios.post(this.backend_url.concat('/client/', this.session_token, '/update/email'), {email: new_email}).then((response) => {
        if (response.status === 200)
          result[0] = true;
        result[1] = response.data;
      }).catch((error) => {
        result[1] = error.message;
      });
      return result;
    },
    async changeUserPassword(new_password) {
      let result = [false, ''];
      await axios.post(this.backend_url.concat('/client/', this.session_token, '/update/password'), {password: new_password}).then((response) => {
        if (response.status === 200)
          result[0] = true;
        result[1] = response.data;
      }).catch((error) => {
        result[1] = error.message;
      });
      return result;
    },
    async updateUserProfile(first_name, second_name, phone_number, birth_date) {
      let result = [false, ''];
      await axios.post(this.backend_url.concat('/client/', this.session_token, '/update/profile'), {
        first_name: first_name,
        second_name: second_name,
        phone_number: phone_number,
        birth_date: birth_date
      }).then((response) => {
        if (response.status === 200)
          result[0] = true;
        result[1] = response.data;
      }).catch((error) => {
        result[1] = error.message;
      });
      return result;
    },
    async logoutUser() {
      let result = [false, ''];
      await axios.put(this.backend_url.concat('/client/', this.session_token, '/logout')).then((response) => {
        if (response.status === 200)
          result[0] = true;
        result[1] = response.data;
      }).catch((error) => {
        result[1] = error.message;
      });
      return result;
    },
    async getUserProfile() {
      let result = [false, ''];
      await axios.get(this.backend_url.concat('/client/', this.session_token, '/get/profile')).then((response) => {
        if (response.status === 200)
          result[0] = true
        result[1] = response.data;
      }).catch((error) => {
        result[1] = error.message;
      });
      return result;
    },
    //todo:
    async sendPasswordResetEmail() {
      let result = [false, ''];
      let email = document.getElementById('passwordEmail').value;
      await axios.get(this.backend_url.concat('/mail/', email, '/send/link')).then((response) => {
        if (response.status === 200)
          result[0] = true;
        result[1] = response.data;
      }).catch((error) => {
        result[1] = error.message;
      });
      return result;
    },
  },
  data() {
    return {
      session_token: null,
      backend_url: 'https://dataroom-301309.ew.r.appspot.com',
    }
  },
}
</script>

<style>
body {
  background-image: url('assets/azure-6.jpg');
}
</style>
