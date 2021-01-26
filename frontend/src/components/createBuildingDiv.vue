<template>
  <form action="javascript:void(0)" v-on:submit="createBuilding" id="createBuildingForm">
    <div class="row">
      <div class="input-field col s6">
        <i class="material-icons prefix">domain</i>
        <input class="validate" id="createBuildingName" type="text" required>
        <label for="createBuildingName" data-error="wrong" data-success="right">Building name</label>
      </div>
      <div class="input-field col s6">
        <button type="submit" class="btn blue darken-1">Create building</button>
      </div>
    </div>
  </form>
</template>

<script>
import M from 'materialize-css';
export default {
  name: "createBuildingDiv",
  methods: {
    async createBuilding() {
      const building_name = document.getElementById('createBuildingName').value;
      const result = await this.$root.createBuilding(building_name);
      if (result[0] === true)
        M.toast({ html: 'Building has been created', classes: "rounded green", displayLength: 2000 });
      else
        M.toast({ html: result[1], classes: "rounded orange", displayLength: 2000 });
    }
  }
}
</script>

<style scoped>

</style>