<template>
  <div class="center-align">
    <a href="javascript:void(0)" v-on:click="currently.building = null; currently.floor = null; currently.room = null;"><span v-if="currently.building">{{ currently.building["building_name"] }}</span></a>
    <span v-if="currently.floor"> > <a href="javascript:void(0)" v-on:click="currently.floor = null; currently.room = null">{{ currently.floor["floor_name"] }}</a></span>
    <span v-if="currently.room"> > <a href="javascript:void(0)" v-on:click="currently.room = null">{{ currently.room['room_name'] }}</a></span>
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
  <div v-else-if="currently.building !== null && currently.floor === null" class="col s4">
    <h3 class="center-align title">Choose floor</h3>
    <ul>
      <li v-for="(item, index) in list.floor_list" :key="index" class="list_item">
        <a v-if="item['isAdmin'] === true || item['isUser'] === true || item['isSuper'] === true || item['public'] === true" href="javascript:void(0)" v-on:click="enterFloor(item)">
          {{ item["floor_name"] }}
        </a>
        <a v-else>{{  item["floor_name"] }} [X]</a>
      </li>
    </ul>
  </div>
  <div v-else-if="currently.floor !== null && currently.room === null" class="col s4">
    <h3 class="center-align title">Choose room</h3>
    <ul>
      <li v-for="(item, index) in list.room_list" :key="index" class="list_item">
        <a href="javascript:void(0)" v-on:click="enterRoom(item)" >{{ item['room_name'] }}</a>
      </li>
    </ul>
    <div v-if="this.currently.floor['isAdmin'] === true" class="row">
      <hr style="color:deepskyblue; width: 70%"/>
        <h5>Floor administrator panel</h5>
      <button v-on:click="changeActiveForm('createRoom')" type="button" class="btn blue darken-2">Create room</button>
      <button v-on:click="changeActiveForm('deleteRoom')" type="button" class="btn blue lighten-2">Delete room</button>
      <button v-on:click="changeActiveForm('manageRoomPermission')" type="button" class="btn blue darken-2">Manage room permissions</button>
      <button v-on:click="changeActiveForm('manageFloorPermission')" type="button" class="btn blue lighten-2">Manage floor permissions</button>
    </div>
    <div v-else-if="this.currently.floor['everybodyCanCreateRoom'] === true">
      <button v-on:click="changeActiveForm('createRoom')" type="button" class="btn blue darken-2">Create room</button>
    </div>
    <form action="javascript:void(0)" v-on:submit="addRoom" id="CREATE_ROOM_FORM" v-if="activeForm === 'createRoom'">
      <div class="row">
        <div class="input-field col s6">
          <i class="material-icons prefix">domain</i>
          <input class="validate" id="createRoomName" type="text" required/>
          <label for="createRoomName" class="active">Room name</label>
        </div>
        <div class="col s6">
          <div class="row input-field" style="margin-bottom: 25px;">
            <input type="checkbox" id="createRoomPermission_public"/>
            <label for="createRoomPermission_public">Public</label>
          </div>
          <div class="row input-field" style="margin-bottom: 25px;">
            <input type="checkbox" id="createRoomPermission_hidden"/>
            <label for="createRoomPermission_hidden">Hidden</label>
          </div>
        </div>
        <div class="input-field col s6">
          <button type="submit" class="btn blue">Create room</button>
        </div>
      </div>
    </form>
    <form action="javascript:void(0)" v-on:submit="deleteRoom" id="DELETE_ROOM_FORM" v-if="activeForm === 'deleteRoom'">
      <div class="col s10">
        <select id="deleteRoomSelect" v-model="DELETE_ROOM_DATA.selected_room_to_delete">
          <option value="" disabled>Select room to delete</option>
          <option v-for="(item, index) in DELETE_ROOM_DATA.room_list" :key="index" :value="item">{{item}}</option>
        </select>
        <button v-if="DELETE_ROOM_DATA.selected_room_to_delete !== ''" type="submit" class="btn blue">Delete room</button>
      </div>
    </form>
    <form action="javascript:void(0)"  id="MANAGE_FLOOR_PERMISSION_FORM" v-if="activeForm === 'manageFloorPermission'">
      <div class="row">
        <div class="col s6">
          <select id="addUToFloorSelect" v-model="MANAGE_FLOOR_PERMISSION_DATA.selected_user_to_add_to_floor">
            <option value="" disabled>Select user to add</option>
            <option v-for="(item, index) in MANAGE_FLOOR_PERMISSION_DATA.building_users_not_in_floor" :key="index" :value="item">{{item['email']}} - {{item['first_name']}} {{item['second_name']}}</option>
          </select>
          <button v-if="MANAGE_FLOOR_PERMISSION_DATA.selected_user_to_add_to_floor !== ''" v-on:click="addUserToFloor" type="button" class="btn blue">Add user to floor</button>
        </div>
        <div class="col s6">
          <select id="removeUFromFloorSelect" v-model="MANAGE_FLOOR_PERMISSION_DATA.selected_user_to_remove_from_floor">
            <option value="" disabled>Select user to delete</option>
            <option v-for="(item, index) in MANAGE_FLOOR_PERMISSION_DATA.floor_users" :key="index" :value="item">{{item['email']}} - {{item['first_name']}} {{item['second_name']}}</option>
          </select>
          <button v-if="MANAGE_FLOOR_PERMISSION_DATA.selected_user_to_remove_from_floor !== ''" v-on:click="deleteUserFromFloor" type="button" class="btn blue">Delete user from floor</button>
        </div>
      </div>
    </form>
    <form action="javascript:void(0)" id="MANAGE_ROOM_PERMISSION_FORM" v-if="activeForm === 'manageRoomPermission'">
      <div class="col s10">
          <select id="managePermissionSelectRoom" v-model="MANAGE_ROOM_PERMISSION_DATA.selected_room" v-on:change="selectRoomToManage">
            <option value="" disabled>Select room to manage</option>
            <option v-for="(item, index) in MANAGE_ROOM_PERMISSION_DATA.room_list" :key="index" :value="item">{{ item }}</option>
          </select>
      </div>
      <div class="row" v-if="MANAGE_ROOM_PERMISSION_DATA.selected_room !== ''">
        <hr style="color: deepskyblue; width: 75%;">
        <div class="col s6">
          <div id="settings">
            <h6>Room settings</h6>
            <div class="col s6">
            <div class="row input-field" style="margin-left: 25px; margin-bottom: 25px;">
              <input type="checkbox" id="managePermission_public" v-model="MANAGE_ROOM_PERMISSION_DATA.selected_setting_public"/>
              <label for="managePermission_public">Public</label>
            </div>
            <div class="row input-field" style="margin-left: 25px; margin-bottom: 25px;">
              <input type="checkbox" id="managePermission_hidden" v-model="MANAGE_ROOM_PERMISSION_DATA.selected_setting_hidden"/>
              <label for="managePermission_hidden">Hidden</label>
            </div>
          </div>
            <div class="col s6">
            <div class="row"/>
            <div class="row"/>
            <button type="button" class="btn blue" v-on:click="updateRoomSettings" style="margin-bottom: 25px;">Update settings</button>
          </div>
          </div>
        </div>
        <div class="col s6">
          <div id="deleteFRoom">
            <h6>Delete user from room</h6>
            <select id="deleteUserFromRoomSelect" v-model="MANAGE_ROOM_PERMISSION_DATA.selected_user_to_remove_from_room">
              <option value="" disabled>Select user to remove from room</option>
              <option v-for="(item, index) in MANAGE_ROOM_PERMISSION_DATA.room_users" :key="index" :value="item">{{item['email']}} - </option>
            </select>
            <button type="button" class="btn blue" v-on:click="removeUserFromRoom">Remove user from room</button>
          </div>
        </div>
      </div>
      <div class="row" v-if="MANAGE_ROOM_PERMISSION_DATA.selected_room !== ''">
        <hr style="color:deepskyblue; width: 70%"/>
        <h6>Add user to room</h6>
        <div class="col s10">
          <select id="addUserToRoomSelect" v-model="MANAGE_ROOM_PERMISSION_DATA.selected_user_to_add_to_room">
            <option value="" disabled>Select user to add to room</option>
            <option v-for="(item, index) in MANAGE_ROOM_PERMISSION_DATA.floor_users_not_in_room" :key="index" :value="item">{{item['email']}}</option>
          </select>
          <div class="row input-field">
            <div class="col s6">
              <input type="checkbox" id="addUserToFloor_permission_download" v-model="MANAGE_ROOM_PERMISSION_DATA.selected_setting_download"/>
              <label for="addUserToFloor_permission_download">User can delete files</label>
            </div>
            <div class="col s6">
              <input type="checkbox" id="addUserToFloor_permission_upload" v-model="MANAGE_ROOM_PERMISSION_DATA.selected_setting_upload"/>
              <label for="addUserToFloor_permission_upload">User can upload files</label>
            </div>
          </div>
          <button type="button" class="btn blue" v-on:click="addUserToRoom">Add user to room</button>
        </div>
      </div>
    </form>
  </div>
  <div v-else-if="currently.room !== null && list.file_list !== null" class="col s4">
    <ul>
      <li v-for="(item, index) in list.file_list" :key="index">
        {{ item }} <a href="javascript:void(0)" v-on:click="downloadFile(item)">DOWNLOAD</a> <a href="javascript:void(0)" v-on:click="deleteFile(item)">DELETE</a>
      </li>
    </ul>
    <input id="uploadFileInput" type="file"/>
    <button type="button" class="btn blue" v-on:click="uploadFile">UPLOAD FILE</button>
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
import _ from 'lodash';

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
      },
      DELETE_ROOM_DATA: {
        selected_room_to_delete: '',
        room_list: '',
      },
      MANAGE_FLOOR_PERMISSION_DATA: {
        building_users_not_in_floor: '',
        selected_user_to_add_to_floor: '',
        selected_user_to_remove_from_floor: '',
        floor_users: '',
      },
      MANAGE_ROOM_PERMISSION_DATA: {
        selected_room: '',
        room_list: '',
        selected_setting_public: '',
        selected_setting_hidden: '',
        selected_user_to_remove_from_room: '',
        room_users: '',
        selected_user_to_add_to_room: '',
        floor_users_not_in_room: '',
        selected_setting_download: '',
        selected_setting_upload: '',
      },
      ROOM_SECTION: {
        activeView: '',
      }
    }
  },
  methods: {
    async changeActiveForm(what) {
      if (this.activeForm === what)
        this.activeForm = '';
      else {
        this.activeForm =  what;
        if (this.activeForm === 'deleteRoom') {
          await this.$root.getFloorRooms(this.currently.floor["floor_name"], this.currently.building["building_name"]).then((response) => {
            if (response[0] === true) {
              this.DELETE_ROOM_DATA.room_list= response[1];
            } else
              M.toast({html: response[1], classes: "rounded orange", displayLength: 2000});
          });
          await setTimeout(null, 500);
          M.FormSelect.init(await document.getElementById('deleteRoomSelect'));
        }
        else if (this.activeForm === 'manageRoomPermission') {
          await this.$root.getFloorRooms(this.currently.floor["floor_name"], this.currently.building["building_name"]).then((response) => {
            if (response[0] === true) {
              this.MANAGE_ROOM_PERMISSION_DATA.room_list= response[1];
            } else
              M.toast({html: response[1], classes: "rounded orange", displayLength: 2000});
          });
          await setTimeout(null, 500);
          M.FormSelect.init(document.getElementById('managePermissionSelectRoom'));
        }
        else if (this.activeForm === 'manageFloorPermission') {
          let floor_xml;
          await this.$root.LEVELADMIN_get_floor_xml(this.currently.building['building_name'], this.currently.floor['floor_name']).then((response) => {
            if (response[0] === true)
              floor_xml = response[1];
            else
              M.toast({html: response[1], classes: 'rounded orange', displayLength: 2000});
          });
          let building_users;
          await this.$root.LEVELADMIN_getAllUsersForBuilding(this.currently.building['building_name']).then((response) => {
            if (response[0] === true)
              building_users = response[1];
            else
              M.toast({html: response[1], classes: 'rounded orange', displayLength: 2000});
          });
          const parser = new DOMParser();
          const xml_doc = parser.parseFromString(floor_xml, 'text/xml');
          const users = xml_doc.getElementsByTagName('user');
          this.MANAGE_FLOOR_PERMISSION_DATA.building_users_not_in_floor = await _.filter(building_users, (item) => {
            for (let k = 0; k < users.length; k++) {
              if (Number(users[k].getAttribute('client_id')) === item['id'])
                return false;
            }
            return true;
          });
          this.MANAGE_FLOOR_PERMISSION_DATA.floor_users = await _.filter(building_users, (item) => {
            for (let k = 0; k < users.length; k++) {
              if (Number(users[k].getAttribute('client_id')) === item['id'])
                return true;
            }
            return false;
          });
          await setTimeout(null, 500);
          M.FormSelect.init(document.getElementById('addUToFloorSelect'));
          M.FormSelect.init(document.getElementById('removeUFromFloorSelect'));
        }
      }
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
      await this.$root.getFilesInRoom(room_name['room_name'], this.currently.building["building_name"], this.currently.floor["floor_name"]).then((response) => {
        if (response[0] === true)
          this.list.file_list = response[1];
        else
          M.toast({html: response[1], classes: "rounded orange", displayLength: 2000});
      });
    },
    async enterFloor(floor_item) {
      this.currently.floor = floor_item;
      this.list.room_list = floor_item['room_data'];
    },
    async enterBuilding(asWho) {
      if (this.tmp.val1["isAdmin"] === true)
        M.Modal.getInstance(document.getElementById('buildingEnterAdminOrUser')).close();
      if (asWho === 'user') {
        this.currently.building = this.tmp.val1;
        await this.getFloorList(this.tmp.val1["building_name"])
      } else if (asWho === 'admin') {
        this.$parent.changeView('admin', this.tmp.val1["building_name"]);
      }

    },
    async getBuildingList() {
      await this.$root.getBuildingList().then((response) => {
        if (response[0] === true)
          this.list.building_list = response[1];
        else
          M.toast({html: response[1], classes: "rounded orange", displayLength: 2000});
      });
    },
    async getFloorList(name) {
      await this.$root.getBuildingFloors(name).then((response) => {
        if (response[0] === false)
          M.toast({html: response[1], classes: "rounded orange", displayLength: 2000});
        else
          this.list.floor_list = response[1];
      });
    },
    async addRoom() {
      const roomName = document.getElementById('createRoomName').value;
      const perm_public = document.getElementById('createRoomPermission_public').checked;
      const perm_hidden = document.getElementById('createRoomPermission_hidden').checked;
      await this.$root.LEVELADMIN_createRoom(roomName, this.currently.floor["floor_name"], this.currently.building["building_name"], perm_public, perm_hidden).then(async (response) => {
        if (response[0] === true) {
          M.toast({html: 'Room has been created', classes: "rounded green", displayLength: 2000});
          await this.enterFloor(this.currently.floor);
          this.activeForm = '';
        } else
          M.toast({html: response[1], classes: "rounded orange", displayLength: 2000});
      });
    },
    async deleteRoom() {
      await this.$root.LEVELADMIN_deleteRoom(this.currently.building['building_name'], this.currently.floor['floor_name'], this.DELETE_ROOM_DATA.selected_room_to_delete).then(async (response) => {
        if (response[0] === true) {
          M.toast({html: 'Room has been deleted', classes: 'rounded green', displayLength: 2000});
          await this.enterFloor(this.currently.floor);
          this.activeForm = '';
        } else
          M.toast({html: response[1], classes: 'rounded orange', displayLength: 2000});
      });
    },
    async addUserToFloor() {
      const parser = new DOMParser();
      let xml_string;
      await this.$root.LEVELADMIN_get_floor_xml(this.currently.building['building_name'], this.currently.floor['floor_name']).then((response) => {
        if (response[0] === true)
          xml_string = response[1];
        else
          M.toast({html: response[1], classes: 'rounded orange', displayLength: 2000});
      });
      let xml_doc = parser.parseFromString(xml_string, 'text/xml');
      let new_node = xml_doc.createElement('user');
      new_node.setAttribute('client_id', String(this.MANAGE_FLOOR_PERMISSION_DATA.selected_user_to_add_to_floor['id']));
      xml_doc.getElementsByTagName('users')[0].appendChild(new_node);
      await this.$root.LEVELADMIN_update_floor_xml(this.currently.building['building_name'], this.currently.floor['floor_name'], xml_doc).then(async (response) => {
        if (response[0] === true) {
          M.toast({html: 'User has been added to floor', classes: 'rounded green', displayLength: 2000});
          this.MANAGE_FLOOR_PERMISSION_DATA = {
            building_users_not_in_floor: '',
            selected_user_to_add_to_floor: '',
            selected_user_to_remove_from_floor: '',
            floor_users: ''};
          await this.changeActiveForm('');
        } else
          M.toast({html: response[1], classes: 'rounded orange', displayLength: 2000});
      });
    },
    async deleteUserFromFloor() {
      const parser = new DOMParser();
      let xml_string;
      await this.$root.LEVELADMIN_get_floor_xml(this.currently.building['building_name'], this.currently.floor['floor_name']).then((response) => {
        if (response[0] === true)
          xml_string = response[1];
        else
          M.toast({html: response[1], classes: 'rounded orange', displayLength: 2000});
      });
      let xml_doc = parser.parseFromString(xml_string, 'text/xml');
      let users = xml_doc.getElementsByTagName('user');
      let i = 0;
      for (; i < users.length; i++) {
        if (Number(users[i].getAttribute('client_id')) === this.MANAGE_FLOOR_PERMISSION_DATA.selected_user_to_remove_from_floor['id']) {
          break;
        }
      }
      users[i].parentNode.removeChild(users[i]);
      await this.$root.LEVELADMIN_update_floor_xml(this.currently.building['building_name'], this.currently.floor['floor_name'], xml_doc).then(async (response) => {
        if (response[0] === true) {
          M.toast({html: 'User has been removed from floor', classes: 'rounded green', displayLength: 2000});
          this.MANAGE_FLOOR_PERMISSION_DATA = {
            building_users_not_in_floor: '',
            selected_user_to_add_to_floor: '',
            selected_user_to_remove_from_floor: '',
            floor_users: ''};
          await this.changeActiveForm('');
        } else M.toast({html: response[1], classes: 'rounded orange', displayLength: 2000});
      });
    },
    async selectRoomToManage() {
      let building_users;
      let xml_string;
      await this.$root.LEVELADMIN_get_floor_xml(this.currently.building['building_name'], this.currently.floor['floor_name']).then((response) => {
        if (response[0] === true)
          xml_string = response[1];
        else
          M.toast({ html: response[1], classes: 'rounded orange', displayLength: 2000 });
      });
      await this.$root.LEVELADMIN_getAllUsersForBuilding(this.currently.building['building_name']).then((response) => {
        if (response[0] === true)
          building_users = response[1];
        else
          M.toast({html: response[1], classes: 'rounded orange', displayLength: 2000});
      });
      const parser = new DOMParser();
      const xml_doc = parser.parseFromString(xml_string, 'text/xml');
      const rooms = xml_doc.getElementsByTagName('room');
      let i = 0;
      for (; i < rooms.length; i++) {
        if (rooms[i].getAttribute('room_name') === this.MANAGE_ROOM_PERMISSION_DATA.selected_room)
          break;
      }
      (rooms[i].getAttribute('public') === 'True') ? this.MANAGE_ROOM_PERMISSION_DATA.selected_setting_public = true : this.MANAGE_ROOM_PERMISSION_DATA.selected_setting_public = false;
      (rooms[i].getAttribute('hidden') === 'True') ? this.MANAGE_ROOM_PERMISSION_DATA.selected_setting_hidden = true : this.MANAGE_ROOM_PERMISSION_DATA.selected_setting_hidden = false;
      const users_in_room = rooms[i].getElementsByTagName('user');
      this.MANAGE_ROOM_PERMISSION_DATA.floor_users_not_in_room = await _.filter(building_users, (item) => {
        for (let j = 0; j < users_in_room.length; j++) {
          if (Number(item['id'] === Number(users_in_room[j].getAttribute('client_id'))))
            return false;
        }
        return true;
      });
      this.MANAGE_ROOM_PERMISSION_DATA.room_users = await _.filter(building_users, (item) => {
        for (let j = 0; j < users_in_room.length; j++) {
          if (Number(item['id'] === Number(users_in_room[j].getAttribute('client_id'))))
            return true;
        }
        return false;
      });
      await setTimeout(null, 500);
      M.FormSelect.init(document.getElementById('addUserToRoomSelect'));
      M.FormSelect.init(document.getElementById('deleteUserFromRoomSelect'));
    },
    async updateRoomSettings() {
      let xml_string;
      await this.$root.LEVELADMIN_get_floor_xml(this.currently.building['building_name'], this.currently.floor['floor_name']).then((response) => {
        if (response[0] === true)
          xml_string = response[1];
        else
          M.toast({html: response[1], classes: 'rounded orange', displayLength: 2000});
      });
      const parser = new DOMParser();
      let root = parser.parseFromString(xml_string, 'text/xml');
      let rooms = root.getElementsByTagName('room');
      for (let i = 0; i < rooms.length; i++) {
        if (rooms[i].getAttribute('room_name') === this.MANAGE_ROOM_PERMISSION_DATA.selected_room) {
          (this.MANAGE_ROOM_PERMISSION_DATA.selected_setting_public === true) ? rooms[i].setAttribute('public', 'True') : rooms[i].setAttribute('public', 'False');
          (this.MANAGE_ROOM_PERMISSION_DATA.selected_setting_hidden === true) ? rooms[i].setAttribute('hidden', 'True') : rooms[i].setAttribute('hidden', 'False');
        }
      }
      await this.$root.LEVELADMIN_update_floor_xml(this.currently.building['building_name'], this.currently.floor['floor_name'], root).then(async (response) => {
        if (response[0] === true) {
          M.toast({html: 'Room settings has been updated', classes: 'rounded green', displayLength: 2000});
          await this.changeActiveForm('');
          this.MANAGE_ROOM_PERMISSION_DATA = {
            selected_room: '',
            room_list: '',
            selected_setting_public: '',
            selected_setting_hidden: '',
            selected_user_to_remove_from_room: '',
            room_users: '',
            selected_user_to_add_to_room: '',
            floor_users_not_in_room: '',
            selected_setting_download: '',
            selected_setting_upload: '',
          }
        } else
          M.toast({html: response[1], classes: 'rounded orange', displayLength: 2000});
      });
    },
    async addUserToRoom() {
      let xml_string;
      await this.$root.LEVELADMIN_get_floor_xml(this.currently.building['building_name'], this.currently.floor['floor_name']).then((response) => {
        if (response[0] === true)
          xml_string = response[1];
        else
          M.toast({html: response[1], classes: 'rounded orange', displayLength: 2000});
      });
      const parser = new DOMParser();
      const root = parser.parseFromString(xml_string, 'text/xml');
      const rooms = root.getElementsByTagName('room');
      let i = 0;
      for (; i < rooms.length; i++) {
        if (rooms[i].getAttribute('room_name') === this.MANAGE_ROOM_PERMISSION_DATA.selected_room)
          break;
      }
      let new_node = root.createElement('user');
      new_node.setAttribute('client_id', String(this.MANAGE_ROOM_PERMISSION_DATA.selected_user_to_add_to_room['id']));
      new_node.setAttribute('download', (this.MANAGE_ROOM_PERMISSION_DATA.selected_setting_download === true) ? "True" : "False");
      new_node.setAttribute('upload', (this.MANAGE_ROOM_PERMISSION_DATA.selected_setting_upload === true) ? "True" : "False");
      rooms[i].appendChild(new_node);
      await this.$root.LEVELADMIN_update_floor_xml(this.currently.building['building_name'], this.currently.floor['floor_name'], root).then(async (response) => {
        if (response[0] === true) {
          M.toast({ html: 'User has been added to room' });
          await this.changeActiveForm('');
          this.MANAGE_ROOM_PERMISSION_DATA = {
            selected_room: '',
            room_list: '',
            selected_setting_public: '',
            selected_setting_hidden: '',
            selected_user_to_remove_from_room: '',
            room_users: '',
            selected_user_to_add_to_room: '',
            floor_users_not_in_room: '',
            selected_setting_download: '',
            selected_setting_upload: '',
          }
        } else
          M.toast({ html: response[1], classes: 'rounded orange', displayLength: 2000 });
      })
    },
    async removeUserFromRoom() {
      let xml_string;
      await this.$root.LEVELADMIN_get_floor_xml(this.currently.building['building_name'], this.currently.floor['floor_name']).then((response) => {
        if (response[0] === true)
          xml_string = response[1];
        else
          M.toast({html: response[1], classes: 'rounded orange', displayLength: 2000});
      });
      const parser = new DOMParser();
      let root = parser.parseFromString(xml_string, 'text/xml');
      let rooms = root.getElementsByTagName('room');
      let i = 0;
      for(; i < rooms.length ; i++) {
        if (rooms[i].getAttribute('room_name') === this.MANAGE_ROOM_PERMISSION_DATA.selected_room)
          break;
      }
      let users_in_room = rooms[i].getElementsByTagName('user');
      let j = 0;
      for(; j < users_in_room.length; j++) {
        if (Number(users_in_room[j].getAttribute('client_id')) === this.MANAGE_ROOM_PERMISSION_DATA.selected_user_to_remove_from_room['id'])
          break;
      }
      users_in_room[j].parentNode.removeChild(users_in_room[j]);
      await this.$root.LEVELADMIN_update_floor_xml(this.currently.building['building_name'], this.currently.floor['floor_name'], root).then(async (response) => {
        if (response[0] === true) {
          M.toast({html: 'User has been removed from floor', classes: 'rounded green', displayLength: 2000});
          this.MANAGE_ROOM_PERMISSION_DATA = {
            building_users_not_in_floor: '',
            selected_user_to_add_to_floor: '',
            selected_user_to_remove_from_floor: '',
            floor_users: ''};
          await this.changeActiveForm('');
        } else M.toast({html: response[1], classes: 'rounded orange', displayLength: 2000});
      });
    },
    async uploadFile() {
      const file = document.getElementById('uploadFileInput');
      if (file.files[0] === undefined)
        M.toast({ html: 'You have to select file to upload ', classes: 'rounded orange', displayLength: 2000 });
      else {
        await this.$root.USER_uploadFile(this.currently.building['building_name'], this.currently.floor['floor_name'], this.currently.room['room_name'], file).then(async (response) => {
          if (response[0] === true) {
            M.toast({html: 'File has been uploaded', classes: 'rounded green', displayLength: 2000});
            document.getElementById('uploadFileInput').value = '';
            await this.enterRoom(this.currently.room);
          } else
            M.toast({html: response[1], classes: 'rounded orange', displayLength: 2000});
        });
      }
    },
    async downloadFile(item) {
      await this.$root.USER_download_file(this.currently.building['building_name'], this.currently.floor['floor_name'], this.currently.room['room_name'], item).then((response) => {
        if (response[0] !== true)
          M.toast({ html: 'Cannot download this file', classes: 'rounded green', displayLength: 2000 });
      });
    },
    async deleteFile(item) {
      await this.$root.USER_remove_file(this.currently.building['building_name'], this.currently.floor['floor_name'], this.currently.room['room_name'], item).then(async (response) => {
        if (response[0] === true) {
          M.toast({html: 'File has been removed', classes: 'rounded green', displayLength: 2000});
          await this.enterRoom(this.currently.room);
        }
        else
          M.toast({ html: response[1], classes: 'rounded orange', displayLength: 2000 });
      });

    }
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