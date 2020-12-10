<template>
  <div class="col s2">
    <ul id="slide-out" class="side-nav fixed center-align">
      <li><div class="blue darken-2 white-text" style="border-radius: 20px; box-shadow: 2px 2px 2px 2px #468199">
        <i>Logged as</i><br>
        <b>{{this.$root.$data.fb.auth().currentUser.email}}</b>
      </div></li>
      <li><div class="divider"></div></li>
      <li><button type="button" @click="this.$parent.changeView('dashBoard')" class="btn blue">DashBoard</button></li>
      <li><div class="divider"></div></li>
      <li><button type="button" @click="this.$parent.changeView('tokenInfo')" class="btn blue">Show my tokens</button></li>
      <li><div class="divider"></div></li>
      <li><button type="button" @click="this.$parent.changeView('profileSettings')" class="btn blue">Profile Settings</button></li>
      <li><div class="divider"></div></li>
      <li><button type="button" @click=this.$parent.logout class="btn blue">Logout and exit app</button></li>
      <li><div class="divider"></div></li>
    </ul>
  </div>
</template>

<script>
export default {
name: 'sideBar'
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