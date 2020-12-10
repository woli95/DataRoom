<!--TODO:
1. Przekierowanie z pomyślnej rejestracji
2. Przekierowanie z pomyślnego logowania -->


<template>
  <LoginView v-if="logged === false" />
  <AppView v-if="logged === true" />
</template>

<script>
import LoginView from "@/components/LoginView.vue";
import AppView from "@/components/AppView";
import firebase from 'firebase';

// const bu = 'https://data-room-293312.ew.r.appspot.com';
const bu_local =  'http://127.0.0.1:5000';
const firebaseConfig = {
  apiKey: "AIzaSyDZt4vzBei774pUJLNvwI3VQJjsUOvkY-o",
  authDomain: "data-room-293312.firebaseapp.com",
  databaseURL: "https://data-room-293312.firebaseio.com",
  projectId: "data-room-293312",
  storageBucket: "data-room-293312.appspot.com",
  messagingSenderId: "85427468926",
  appId: "1:85427468926:web:e2ef214971d39f34ac362f"
};
firebase.initializeApp(firebaseConfig)

export default {
  name: 'App',
  computed: {
    console: () => console
  },
  components: {
    AppView,
    LoginView,
  },
  methods: {
    async isLoggedIn() {
      if (await firebase.auth().currentUser != null) {
        this.logged = true;
      } else {
        this.logged = false;
      }
    },
  },
  data() {
    return {
      appView: false,
      loginView: true,
      fb: firebase,
      logged: false,
      backend_url: bu_local,
    }
  },
  async mounted() {
    await this.isLoggedIn();
  },
}
</script>

<style>
body {
  background-image: url('assets/azure-6.jpg');
}
</style>
