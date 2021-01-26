<template>
  <div class="center-align">
    <span v-if="currently.building">{{ currently.building["building_name"] }}</span>
    <span v-if="currently.floor"> > {{ currently.floor["floor_name"] }}</span>
    <span v-if="currently.room"> > {{ currently.room }}</span>
  </div>
  <div v-if="currently.building === null" class="col s4 buildingList">
    <h3 class="center-align title">Choose building</h3>
    <ul>
      <li v-for="(item, index) in list.building_list" :key="index" class="list_item">
        <a href="javascript:void(0)" v-on:click="selectBuilding(item)">
          {{ item["building_name"] }}
        </a>
      </li>
    </ul>
  </div>
  <div v-if="currently.building !== null && currently.floor === null" class="col s4">
    <h3 class="center-align title">Choose floor</h3>
    <ul>
      <li v-for="(item, index) in list.floor_list" :key="index" class="list_item">
        <a href="javascript:void(0)" v-on:click="enterFloor(item)">
          {{ item["floor_name"] }}
        </a>
      </li>
    </ul>
  </div>
  <div v-if="currently.floor !== null && currently.room === null" class="col s4">
    <h3 class="center-align title">Choose room</h3>
    <ul>
      <li v-for="(item, index) in list.room_list" :key="index" class="list_item">
        <a href="javascript:void(0)" v-on:click="enterRoom(item)" >{{ item }}</a>
      </li>
    </ul>
    <div v-if="this.currently.floor['isAdmin'] === true" class="col s4">
      Your are floor administrator.
      <button v-on:click="changeActiveForm('create')" type="button" class="btn blue">Create room</button>
    </div>
    <form class="col s4" action="javascript:void(0)" v-on:submit="addRoom" id="addRoom" v-if="this.activeForm === 'create'">
      <div class="row">
        <div class="input-field col s4">
          <i class="material-icons prefix">domain</i>
          <input class="validate" id="createRoomName" type="text" required/>
          <label for="createRoomName" class="active">Room name</label>
        </div>
      </div>
      <div class="row">
        <div class="input-field col s4">
          <button type="submit" class="btn waves-effect waves-light col s12">Create room</button>
        </div>
      </div>
    </form>
  </div>
  <div v-if="currently.room !== null && list.file_list !== null" class="col s4">
    <ul>
      <li v-for="(item, index) in list.file_list" :key="index">
        {{ item }}
      </li>
    </ul>
  </div>
  <div id="buildingEnterAdminOrUser" class="modal">
    <div class="modal-content">
      <h4 class="center-align blue-text text-darken-3">Enter building as:</h4>
      <button type="button" v-on:click="enterBuilding('user')" class="btn btn-large blue lighten-2 left" style="width:125px;">User</button>
      <button type="button" v-on:click="enterBuilding('admin')" class="btn btn-large blue darken-2 right" style="width:125px;">Admin</button>
      <div class="row"/>
    </div>
  </div>
</template>

<script>
import M from 'materialize-css';
export default {
  name: "enterBuildingDiv",
  data() {
    return {
      activeForm: '',
      list: {
        building_list: null,
        floor_list: null,
        room_list: null,
        file_list: null,
      },
      currently: {
        building: null,
        floor: null,
        room: null,
      },
      tmp: {
        val1: null,
      }
    }
  },
  methods: {
    changeActiveForm(what) {
      if (this.activeForm === what)
        this.activeForm = '';
      else
        this.activeForm = what;
    },
    selectBuilding(building_item) {
      this.tmp.val1 = building_item;
      if (building_item["isAdmin"] === false)
        this.enterBuilding('user');
      else if (building_item["isAdmin"] === true)
        M.Modal.init(document.getElementById('buildingEnterAdminOrUser')).open();
    },
    async enterRoom(room_name) {
      this.currently.room = room_name;
      await this.$root.getFilesInRoom(room_name, this.currently.building["building_name"], this.currently.floor["floor_name"]).then((response) => {
        if (response[0] === true)
          this.list.file_list = response[1];
        else
          M.toast({ html: response[1], classes: "rounded orange", displayLength: 2000 });
      });
    },
    async enterFloor(floor_item) {
      this.currently.floor = floor_item;
      await this.$root.getFloorRooms(floor_item["floor_name"], this.currently.building["building_name"]).then((response) => {
        if (response[0] === true) {
          this.list.room_list = response[1];
        }
        else
          M.toast({ html: response[1], classes: "rounded orange", displayLength: 2000 });
      });
    },
    async enterBuilding(asWho) {
      if (this.tmp.val1["isAdmin"] === true)
        M.Modal.getInstance(document.getElementById('buildingEnterAdminOrUser')).close();
      if (asWho === 'user') {
        this.currently.building = this.tmp.val1;
        await this.getFloorList(this.tmp.val1["building_name"])
      }
      else if (asWho === 'admin') {
        this.$parent.changeView('admin', this.tmp.val1["building_name"]);
      }

    },
    async getBuildingList() {
      await this.$root.getBuildingList().then((response) => {
        if (response[0] === true)
          this.list.building_list = response[1];
        else
          M.toast({ html: response[1], classes: "rounded orange", displayLength: 2000 });
      })
    },
    async getFloorList(name) {
      await this.$root.getBuildingFloors(name).then((response) => {
        if (response[0] === false)
          M.toast({ html: response[1], classes: "rounded orange", displayLength: 2000 });
        else
          this.list.floor_list = response[1];
      });
    },
    async addRoom() {
      const roomName = document.getElementById('createRoomName').value;
      await this.$root.addRoomToFloor(roomName, this.currently.floor["floor_name"], this.currently.building["building_name"]).then((response) => {
        if (response[0] === true)
          M.toast({ html: 'Room has been created', classes: "rounded green", displayLength: 2000 });
        else
          M.toast({ html: response[1], classes: "rounded orange", displayLength: 2000 });
      });
    },
  },
  async beforeMount() {
    await this.getBuildingList();
  }
}
</script>

<style scoped>
#buildingEnterAdminOrUser {
  width: 300px;
}

.buildingList {
  margin: 5px;
}
.title {
  color: white;
  background-color: blue;
  padding: 5px;
}
</style>