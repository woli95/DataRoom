<template>
  <div class="row">
    <sideBar class="col s2"/>
  </div>
  <div class="container center">
    <profileSettings v-if="currentView === 'profileSettings'"/>
    <tokenInfo v-if="currentView === 'tokenInfo'"/>
    <dashboard v-if="currentView === 'dashboard'"/>
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
      if (this.currentView === what)
        this.currentView = '';
      else
        this.currentView = what;
    }
  },
  data() {
    return {
      currentView: null,
    }
  },
  computed: {
    console: () => console,
  },
}
</script>

<style scoped>

</style>