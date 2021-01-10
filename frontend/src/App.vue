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
    async registerUser() {
      let result = [false, ''];
      let email = document.getElementById('registerEmail').value;
      let password = document.getElementById('registerPassword').value;
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
    async sendPasswordResetEmail() {
      let result = [false, ''];
      let email = document.getElementById('passwordEmail').value;
      await axios.get(this.backend_url.concat('/mail/', email, '/send')).then((response) => {
        if (response.status === 200)
          result[0] = true;
        result[1] = response.data;
      }).catch((error) => {
        result[1] = error.message;
      });
      return result;
    },
    async loginUser() {
      let result = [false, ''];
      let email = document.getElementById('loginEmail').value;
      let password = document.getElementById('loginPassword').value;
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
    }
  },
  data() {
    return {
      session_token: null,
      backend_url: 'http://127.0.0.1:5000',
    }
  },
}
</script>

<style>
body {
  background-image: url('assets/azure-6.jpg');
}
</style>
