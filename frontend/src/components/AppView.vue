<template>
  <div class="row">
    <sideBar/>
    <div class="col s10">
      <profileSettings v-if="profileSettingsVisibility" class="col s5" style="margin: 10px 10px 10px 10px"/>
      <tokenInfo v-if="tokenInfoViewVisibility" class="col s5" style="margin: 10px 10px 10px 10px"/>
      <div class="row">
        <dashboard v-if="dashboardVisibility" class="col s10" style="margin: 10px 10px 10px 10px"/>
      </div>
    </div>
  </div>
</template>

<script>
import profileSettings from '@/components/profileSettings';
import sideBar from '@/components/sideBar';
import tokenInfo from '@/components/tokenInfo';
import dashboard from '@/components/dashboard';


export default {
  name: "AppView",
  components: {
    dashboard,
    profileSettings,
    sideBar,
    tokenInfo,
  },
  methods: {
    openView(what) {
      if (what === 'tokenInfo')
        this.tokenInfoViewVisibility = !this.tokenInfoViewVisibility;
      else if (what === 'profileSettings')
        this.profileSettingsVisibility = !this.profileSettingsVisibility;
      else if (what === 'dashboard')
        this.dashboardVisibility = !this.dashboardVisibility;
    }
  },
  data() {
    return {
      tokenInfoViewVisibility: false,
      profileSettingsVisibility: false,
      dashboardVisibility: false,
    }
  },
  computed: {
    console: () => console,
  },
}
</script>

<style scoped>

</style>