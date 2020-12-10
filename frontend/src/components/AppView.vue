<template>
  <div class="row">
    <sideBar/>
    <div class="col s10">
      <profileSettings v-if="this.profileSettingsView === true" class="col s5"/>
      <tokenInfo v-if="this.tokenInfoView === true" class="col s5"/>
    </div>
  </div>
</template>

<script>
import profileSettings from '@/components/profileSettings';
import sideBar from '@/components/sideBar';
import tokenInfo from '@/components/tokenInfo';

import axios from 'axios';
import M from 'materialize-css';

export default {
  name: "AppView",
  components: {
    profileSettings,
    sideBar,
    tokenInfo,
  },
  methods: {
    async logout() {
      await axios.post(this.$root.$data.backend_url.concat('/client/', this.$root.$data.fb.auth().currentUser.uid.toString(), '/logout')).then(async (response) => {
        if (response.data === 'OK') {
          M.toast({ html: 'Tokens destroyed', classes: 'rounded blue', displayLength: 2000 });
          await this.$root.$data.fb.auth().signOut().then(() => {
            M.toast({ html: 'Signed out', classes: 'rounded blue', displayLength: 2000 });
            this.$root.$data.logged = false;
            this.$root.$data.LoginView = true;
            this.$root.$data.AppView = false;
          });
        }
      });
    },
    changeView(view) {
      if(view === 'profileSettings') {
        this.profileSettingsView = !this.profileSettingsView;
      } else if(view === 'dashboard') {
        this.dashboardView = !this.dashboardView;
      } else if(view === 'tokenInfo') {
        this.tokenInfoView = !this.tokenInfoView;
      }
    },
    async getClientInfo() {
      console.log("CALL");
      await axios.get(this.$root.$data.backend_url.concat('/client/', this.$root.$data.fb.auth().currentUser.uid.toString(), '/info')).then((response) => {
        this.currentClientInfo = response.data;
      });
    }
  },
  data() {
    return {
      profileSettingsView: false,
      dashboardView: false,
      tokenInfoView: false,
      currentClientInfo: null
    }
  },
  computed: {
    console: () => console,
  },
  async mounted() {
    await this.getClientInfo();
  }
}
</script>

<style scoped>

</style>