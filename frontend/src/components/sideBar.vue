<template>
  <div>
    <ul id="slide-out" class="side-nav fixed center-align">
      <li><div class="blue darken-2 white-text" style="border-radius: 20px; box-shadow: 2px 2px 2px 2px #468199">
        <i>Logged as</i><br><b>{{clientEmail}}</b>
      </div></li>
      <li><div class="divider"></div></li>
      <li><button type="button" @click="this.$parent.openView('dashboard')" class="btn blue">DashBoard</button></li>
      <li><div class="divider"></div></li>
      <li><button type="button" @click="this.$parent.openView('tokenInfo')" class="btn blue">Show my tokens</button></li>
      <li><div class="divider"></div></li>
      <li><button type="button" @click="this.$parent.openView('profileSettings')" class="btn blue">Profile Settings</button></li>
      <li><div class="divider"></div></li>
      <li><button type="button" @click="buttonClick('logout')" class="btn blue">Logout and exit app</button></li>
      <li><div class="divider"></div></li>
    </ul>
  </div>
</template>

<script>
import M from 'materialize-css';

export default {
  name: 'sideBar',
  data() {
    return {
      clientEmail: '',
    }
  },
  methods: {
    async buttonClick(button) {
      if (button === 'logout') {
        await this.$root.AUTH_logoutUser().then((response) => {
          if (response[0] === true) {
            M.toast({ html: 'You have been logged out', classes: 'rounded green', displayLength: 2000 });
            this.$root.session_token = null;
          } else {
            M.toast({ html: response[1], classes: 'rounded orange', displayLength: 2000 });
          }
        });
      }
    },
  },
  async beforeMount() {
    await this.$root.USER_getUserProfile().then((response) => {
      if (response[0] === true)
        this.clientEmail = response[1][0]["email"];
    });
  }
}
</script>

<style scoped>
#slide-out {
  border-right: 5px outset #468499;
  box-shadow: 4px 4px 4px 4px #468199
}
li {
  margin: 8px;
}
button:hover {
  opacity: 0.8;
}
.divider {
  margin: 5px;
}
ul li:hover {
  background-color: rgba(0, 0, 0, 0) !important;
}
</style>