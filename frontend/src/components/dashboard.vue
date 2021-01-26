<template>
  <div id="main" class="container white">
    <div v-if="!buildingAdminName" class="row">
      <button type="button" v-on:click="changeView('enter')" class="btn blue" style="width:250px; margin:5px">ENTER BUILDING</button>
      <button type="button" v-on:click="changeView('create')" class="btn blue" style="width:250px; margin:5px">CREATE NEW BUILDING</button>
    </div>
    <hr v-if="!buildingAdminName" style="color: deepskyblue"/>
    <enter-building-div v-if="buildingEnterView"/>
    <create-building-div v-if="buildingCreateView"/>
    <admin-building-div v-if="buildingAdminName" :buildingName="buildingAdminName"/>
  </div>
</template>

<script>
import createBuildingDiv from '@/components/createBuildingDiv';
import enterBuildingDiv from '@/components/enterBuildingDiv';
import adminBuildingDiv from '@/components/adminBuildingDiv';
export default {
  name: "dashboard",
  components: {
    createBuildingDiv, enterBuildingDiv, adminBuildingDiv
  },
  data() {
    return {
      buildingEnterView: false,
      buildingCreateView: false,
      buildingAdminName: null,
    }
  },
  methods: {
    changeView(view, buildingName = null) {
      if (view === 'enter') {
        this.buildingEnterView = true;
        this.buildingCreateView = false;
        this.buildingAdminName = null;
      } else if (view === 'create') {
        this.buildingCreateView = true;
        this.buildingEnterView = false;
        this.buildingAdminName = null;
      } else if (view === 'admin') {
        this.buildingCreateView = false;
        this.buildingEnterView = false;
        this.buildingAdminName = buildingName;
        this.$forceUpdate();
      }
    },
  },
}
</script>

<style scoped>
#main {
  border-right: 5px outset #468499;
  box-shadow: 4px 4px 4px 4px #468199
}
</style>