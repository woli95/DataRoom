<template>
  <div class="container">
    <div class="row"/>
    <div class="row" style="margin: 0 !important;">
      <button type="button" v-on:click="changeView('addUser')"  class="btn blue darken-2 col s6">Add user to building</button>
      <button type="button" v-on:click="changeView('removeUser')" class="btn blue lighten-2 col s6">Remove user from building</button>
    </div>
    <div class="row" style="margin: 0 !important;">
      <button type="button" v-on:click="changeView('addFloor')" class="btn blue lighten-2 col s6">Create new floor</button>
      <button type="button" v-on:click="changeView('removeFloor')"  class="btn blue darken-2 col s6">Remove floor</button>
    </div>
    <div class="row" style="margin: 0 !important;">
      <button type="button" v-on:click="changeView('updateFloor')" class="btn blue darken-2 col s6">Update floor settings</button>
      <button type="button" v-on:click="changeView('adminBuilding')" class="btn blue lighten-2 col s6">Manage admin role</button>
    </div>
    <div class="row"/>
    <hr style="color:deepskyblue"/>
    <form v-if="activeView === 'addFloor'" action="javascript:void(0)" v-on:submit="addFloor" id="addFloor">
      <div class="row input-field">
          <i class="material-icons prefix">remove_red_eye</i>
          <input class="validate" id="addFloorName" type="text" required>
          <label for="addFloorName" class="active" >Floor name</label>
      </div>
      <div class="row input-field" style="margin-bottom: 25px;">
          <input type="checkbox" id="addFloorPermission_public"/>
          <label for="addFloorPermission_public">Public</label>
      </div>
      <div class="row input-field" style="margin-bottom: 25px;">
        <input type="checkbox" id="addFloorPermission_hidden"/>
        <label for="addFloorPermission_hidden">Hidden</label>
      </div>
      <div class="row input-field" style="margin-bottom: 25px;">
          <input type="checkbox" id="addFloorPermission_everybody"/>
          <label for="addFloorPermission_everybody">Everybody can create rooms</label>
      </div>
      <div class="row input-field" style="margin-bottom: 25px;">
          <input type="checkbox" id="addFloorPermission_creators"/>
          <label for="addFloorPermission_creators">Creators can remove their rooms</label>
      </div>
      <div class="row"/>
      <div class="row input-field">
        <button type="submit" class="btn btn blue darken-2">CREATE FLOOR</button>
      </div>
    </form>
    <form v-if="activeView === 'removeFloor'" action="javascript:void(0)" v-on:submit="removeFloor" id="removeFloor">
      <div class="row input-field">
        <select id="removeFloorSelect" v-model="removeFloor_data.selectedFloorToRemove">
          <option value="" disabled>Select floor to delete</option>
          <option v-for="(item, index) in removeFloor_data.floor_list" :key="index" :value="item" >{{ item }}</option>
        </select>
      </div>
      <button type="submit" class="btn blue">Remove floor</button>
    </form>
    <form v-if="activeView === 'removeUser'" action="javascript:void(0)" v-on:submit="removeUser" id="removeUser">
      <div class="row input-field">
        <select id="removeUserSelect" v-model="removeUser_data.selectedUserToRemove">
          <option value="" disabled>Select user to remove</option>
          <option v-for="(item, index) in removeUser_data.user_list" :key="index" :value="item['email']" >{{ item['email'] }} - {{ item['first_name'] }} {{ item['second_name'] }}</option>
        </select>
      </div>
      <button type="submit" class="btn blue">Remove user</button>
    </form>
    <form v-if="activeView === 'addUser'" action="javascript:void(0)" v-on:submit="addUser" id="addUser">
      <div class="row input-field">
        <input v-model="addUser_data.emailUserToAdd" type="email" id="addUserEmail" required />
        <label for="addUserEmail" class="active">Enter user email</label>
      </div>
      <button type="submit" class="btn blue">Add user</button>
    </form>
    <form v-if="activeView === 'updateFloor'" action="javascript:void(0)" id="updateFloor">
      <div class="row input-field">
        <select id="updateFloorSelect" v-model="updateFloor_data.selectedFloorToUpdate" v-on:change="getFloorToUpdate">
          <option value="" disabled>Select floor to update</option>
          <option v-for="(item, index) in updateFloor_data.floor_list" :key="index" :value="item">{{ item }}</option>
        </select>
      </div>
      <div v-if="updateFloor_data.data_to_update" class="row">
        <div class="col s6">
          <div class="row input-field" style="margin-bottom: 25px;">
            <input type="checkbox" id="updateFloorPermission_public"/>
            <label for="updateFloorPermission_public">Public</label>
          </div>
          <div class="row input-field" style="margin-bottom: 25px;">
            <input type="checkbox" id="updateFloorPermission_hidden"/>
            <label for="updateFloorPermission_hidden">Hidden</label>
          </div>
          <div class="row input-field" style="margin-bottom: 25px;">
            <input type="checkbox" id="updateFloorPermission_everybody"/>
            <label for="updateFloorPermission_everybody">Everybody can create rooms</label>
          </div>
          <div class="row input-field" style="margin-bottom: 25px;">
            <input type="checkbox" id="updateFloorPermission_creators"/>
            <label for="updateFloorPermission_creators">Creators can remove their rooms</label>
          </div>
        </div>
        <div class="col s6">
          <div class="row"/>
          <div class="row"/>
          <button type="button" v-on:click="updateSettings" class="btn blue">Update settings</button>
        </div>
        <div class="row"/>
        <div class="row">
          <div class="col s6">
            <b>Level administrators:</b>
            <select id="updateFloorLevelAdministratorSelect" v-model="updateFloor_data.selectedLevelAdministrator">
              <option value="" disabled>Select level administrator</option>
              <option v-for="(item, index) in updateFloor_data.level_administrator_list" :key="index" :value="item">{{item['email']}} - {{item['first_name']}} {{item['second_name']}}</option>
            </select>
            <button type="button" v-on:click="removeLevelAdministrator" class="btn blue">Remove level admin</button>
          </div>
          <div class="col s6">
            <b>Users:</b>
            <select id="updateFloorUserSelect" v-model="updateFloor_data.selectedUser">
              <option value="" disabled>Select user</option>
              <option v-for="(item, index) in updateFloor_data.nolevel_administrator_list" :key="index" :value="item">{{item['email']}} - {{item['first_name']}} {{item['second_name']}}</option>
            </select>
            <button type="button" v-on:click="addLevelAdministrator" class="btn blue">Add level admin</button>
          </div>
        </div>
      </div>
    </form>
    <form v-if="activeView === 'adminBuilding'" action="javascript:void(0)" id="adminBuilding">
      <div class="row">
        <div class="col s6">
          <select id="adminBuildingAdminsSelect" v-model="adminBuilding_data.selectedAdmin">
            <option value="" disabled>Select admin</option>
            <option v-for="(item, index) in adminBuilding_data.Admin_list" :key="index" :value="item">{{ item['email']}} - {{ item['first_name']}} {{ item['second_name'] }}</option>
          </select>
          <button type="button" v-on:click="removeAdmin" class="btn blue">Take back admin role form user</button>
        </div>
        <div class="col s6">
          <select id="adminBuildingNoAdminsSelect" v-model="adminBuilding_data.selectedNoAdmin">
            <option value="" disabled>Select user</option>
            <option v-for="(item, index) in adminBuilding_data.noAdmin_list" :key="index" :value="item">{{item['email']}} - {{ item['first_name'] }} {{ item['second_name'] }}</option>
          </select>
          <button type="button" v-on:click="addAdmin" class="btn blue">Add admin role to user</button>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import M from 'materialize-css';
import _ from 'lodash';

export default {
  name: "adminBuildingDiv",
  data() {
    return {
      activeView: '',
      removeFloor_data: {
        floor_list: null,
        selectedFloorToRemove: '',
      },
      addUser_data: {
        emailUserToAdd: '',
      },
      removeUser_data: {
        user_list: null,
        selectedUserToRemove: '',
      },
      updateFloor_data: {
        floor_list: null,
        selectedFloorToUpdate: '',
        data_to_update: null,
        user_list: null,
        selectedLevelAdministrator: '',
        selectedUser: '',
        level_administrator_list: null,
        nolevel_administrator_list: null,
      },
      adminBuilding_data: {
        user_list: null,
        xml_document: null,
        noAdmin_list: null,
        Admin_list: null,
        selectedAdmin: '',
        selectedNoAdmin: '',
      }
    }
  },
  props: {
    buildingName: String,
  },
  methods: {
    async changeView(view) {
      if (view === this.activeView)
        this.activeView = !this.activeView;
      else {
        this.activeView = view;
        if (view === 'removeFloor') {
          await this.$root.ADMIN_getAllFloorsForBuilding(this.buildingName).then((response) => {
            if (response[0] === true)
              this.removeFloor_data.floor_list = response[1];
            else
              M.toast({html: response[1], classes: "rounded orange", displayLength: 2000});
          });
          M.FormSelect.init(document.getElementById('removeFloorSelect'));
        }
        else if (view === 'removeUser') {
          await this.$root.ADMIN_getAllUsersForBuilding(this.buildingName).then( (response) => {
            if (response[0] === true)
              this.removeUser_data.user_list = response[1];
            else
              M.toast({ html: response[1], classes: "rounded orange", displayLength: 2000 });
          });
          M.FormSelect.init(document.getElementById('removeUserSelect'));
        }
        else if (view === 'updateFloor') {
          await this.$root.ADMIN_getAllFloorsForBuilding(this.buildingName).then((response) => {
            if (response[0] === true)
              this.updateFloor_data.floor_list = response[1];
            else
              M.toast({ html: response[1], classes: "rounded orange", displayLength: 2000 });
          });
          await this.$root.ADMIN_getAllUsersForBuilding(this.buildingName).then((response) => {
            if (response[0] === true)
              this.updateFloor_data.user_list = response[1];
            else
              M.toast({ html: response[1], classes: "rounded orange", displayLength: 2000 });
          });
          M.FormSelect.init(document.getElementById('updateFloorSelect'));
        }
        else if (view === 'adminBuilding') {
          await this.$root.ADMIN_getAllUsersForBuilding(this.buildingName).then((response) => {
            if (response[0] === true)
              this.adminBuilding_data.user_list = response[1];
            else
              M.toast({ html: response[1], classes: "rounded orange", displayLength: 2000 });
          });
          await this.$root.ADMIN_getBuildingXML(this.buildingName).then((response) => {
            if (response[0] === true)
              this.adminBuilding_data.xml_document = response[1];
            else
              M.toast({ html: response[1], classes: 'rounded orange', displayLength: 2000});
          });
          const parser = new DOMParser();
          const xml_doc = parser.parseFromString(this.adminBuilding_data.xml_document, 'text/xml');
          let admins = xml_doc.getElementsByTagName('admin');
          let admins_id = []
          for(let i = 0; i < admins.length ; i++)
            admins_id.push(Number(admins[i].attributes[0].value));
          this.adminBuilding_data.Admin_list = await _.filter(this.adminBuilding_data.user_list, (item) => {
            for(let i = 0; i < admins_id.length; i++)
              if (Number(item['id']) === Number(admins_id[i]))
                return true;
            return false;
          });
          this.adminBuilding_data.noAdmin_list = await _.filter(this.adminBuilding_data.user_list, (item) => {
            for(let i = 0; i < admins_id.length; i++)
              if (Number(item['id']) === Number(admins_id[i]))
                return false;
            return true;
          });
          await M.FormSelect.init(document.getElementById('adminBuildingAdminsSelect'));
          await M.FormSelect.init(document.getElementById('adminBuildingNoAdminsSelect'));
        }
      }
    },
    async addFloor() {
      const perm_hidden = document.getElementById('addFloorPermission_hidden').checked;
      const perm_public = document.getElementById('addFloorPermission_public').checked;
      const perm_everybody = document.getElementById('addFloorPermission_everybody').checked;
      const perm_creators = document.getElementById('addFloorPermission_creators').checked;
      if (perm_creators === true && perm_everybody === false) {
        M.toast({ html:"Logic error in permission select. 4rd cannot be checked when 3rd is not checked", classes: "rounded orange", displayLength: 2000})
      } else {
        const name = document.getElementById('addFloorName').value;
        const permissions = [perm_public, perm_hidden, perm_everybody, perm_creators];
        await this.$root.ADMIN_addFloorToBuilding(this.buildingName, name, permissions).then(async (response) => {
          if (response[0] === true) {
            M.toast({html: 'Floor has been created', classes: "rounded green", displayLength: 2000});
            document.getElementById("addFloor").reset();
            await this.changeView('');
          }
          else
            M.toast({ html: response[1], classes: "rounded orange", displayLength: 2000 });
        });
      }
    },
    async removeFloor() {
      if (this.removeFloor_data.selectedFloorToRemove === '') {
        M.toast({ html: 'You have to choose floor to delete', classes: "rounded orange", displayLength: 2000 });
      } else {
        await this.$root.ADMIN_removeFloor(this.buildingName, this.removeFloor_data.selectedFloorToRemove).then(async (response) => {
          if (response[0] === true) {
            M.toast({html: 'Floor has been removed', classes: "rounded green", displayLength: 2000});
            await this.changeView('');
          } else {
            M.toast({html: response[1], classes: "rounded orange", displayLength: 2000});
          }
        });
      }
    },
    async removeUser() {
      if (this.removeUser_data.selectedUserToRemove === '') {
        M.toast({ html: 'You have to choose floor to delete', classes: "rounded orange", displayLength: 2000 });
      } else {
        await this.$root.ADMIN_removeUserFromBuilding(this.buildingName, this.removeUser_data.selectedUserToRemove).then(async (response) => {
          if (response[0] === true) {
            M.toast({html: 'User has been removed', classes: "rounded green", displayLength: 2000});
            await this.changeView('');
          } else
            M.toast({ html: response[1], classes: "rounded orange", displayLength: 2000 });
        });
      }
    },
    async addUser() {
      await this.$root.ADMIN_addUserToBuilding(this.buildingName, this.addUser_data.emailUserToAdd).then(async (response) => {
        if (response[0] === true) {
          M.toast({html: 'User has been added to building', classes: "rounded green", displayLength: 2000});
          await this.changeView('');
        } else
          M.toast({ html: response[1], classes: "rounded orange", displayLength: 2000 });
      });
    },
    async getFloorToUpdate() {
      await this.$root.ADMIN_getFullFloorData(this.buildingName, this.updateFloor_data.selectedFloorToUpdate).then((response) => {
        if (response[0] === true)
          this.updateFloor_data.data_to_update = response[1][0];
        else
          M.toast({ html: response[1], classes:"rounded orange", displayLength: 2000 });
      });
      const parser = new DOMParser();
      const xml_doc = parser.parseFromString(this.updateFloor_data.data_to_update['xml_document'], 'text/xml');
      const settings = xml_doc.getElementsByTagName('setting');
      const perm_sel_pub = document.getElementById('updateFloorPermission_public');
      const perm_sel_hid = document.getElementById('updateFloorPermission_hidden');
      const perm_sel_eve = document.getElementById('updateFloorPermission_everybody');
      const perm_sel_cre = document.getElementById('updateFloorPermission_creators');
      ((settings[0].attributes[0].value === 'True') ? perm_sel_pub.checked = true : perm_sel_pub.checked=false);
      ((settings[1].attributes[0].value === 'True') ? perm_sel_hid.checked = true : perm_sel_hid.checked=false);
      ((settings[2].attributes[0].value === 'True') ? perm_sel_eve.checked = true : perm_sel_eve.checked=false);
      ((settings[3].attributes[0].value === 'True') ? perm_sel_cre.checked = true : perm_sel_cre.checked=false);
      const level_administrators = xml_doc.getElementsByTagName('level_administrator');
      let level_administrators_ids = [];
      for (let i = 0; i < level_administrators.length; i++) {
        level_administrators_ids.push(Number(level_administrators[i].attributes[0].value));
      }
      this.updateFloor_data.level_administrator_list = await _.filter(this.updateFloor_data.user_list, (item) => {
        for(let i = 0; i < level_administrators_ids.length ; i++)
          if(Number(item["id"]) === Number(level_administrators_ids[i]))
            return true
        return false;
      });
      this.updateFloor_data.nolevel_administrator_list = await _.filter(this.updateFloor_data.user_list, (item) => {
        for(let i = 0; i < level_administrators_ids.length ; i++)
          if(Number(item["id"]) === Number(level_administrators_ids[i]))
            return false;
        return true;
      })
      await M.FormSelect.init(document.getElementById('updateFloorLevelAdministratorSelect'));
      await M.FormSelect.init(document.getElementById('updateFloorUserSelect'));
      await this.$forceUpdate();
    },
    async removeLevelAdministrator() {
      const parser = new DOMParser();
      let xml_document = parser.parseFromString(this.updateFloor_data.data_to_update['xml_document'], 'text/xml');
      let elements = xml_document.getElementsByTagName('level_administrator');
      let i = 0;
      for(; i < elements.length; i++) {
        if (Number(elements[i].getAttribute('client_id')) === this.updateFloor_data.selectedLevelAdministrator['id']) {
          break;
        }
      }
      elements[i].parentNode.removeChild(elements[i]);
      await this.$root.ADMIN_update_floor_xml_document(this.buildingName, this.updateFloor_data.selectedFloorToUpdate, xml_document).then(async (response) => {
        if (response[0] === true) {
          M.toast({ html: 'Level administrator role has been deleted', classes: 'rounded green', displayLength: 2000 });
          await this.getFloorToUpdate();
        } else
          M.toast({ html: response[1], classes: 'rounded orange', displayLength: 2000 });
      });
    },
    async addLevelAdministrator() {
      const parser = new DOMParser();
      let xml_document = parser.parseFromString(this.updateFloor_data.data_to_update['xml_document'], 'text/xml');
      let new_node = xml_document.createElement('level_administrator');
      new_node.setAttribute('client_id', this.updateFloor_data.selectedUser['id']);
      xml_document.getElementsByTagName('level_administrator')[0].appendChild(new_node);
      await this.$root.ADMIN_update_floor_xml_document(this.buildingName, this.updateFloor_data.selectedFloorToUpdate, xml_document).then(async (response) => {
        if (response[0] === true) {
          M.toast({html: 'Level administrator has been added', classes: "rounded green", displayLength: 2000});
          await this.getFloorToUpdate();
        }
        else
          M.toast({ html: response[1], classes: "rounded orange", displayLength: 2000 });
      });
    },
    async updateSettings() {
      const new_settings = [document.getElementById('updateFloorPermission_public').checked, document.getElementById('updateFloorPermission_hidden').checked,
      document.getElementById('updateFloorPermission_everybody').checked, document.getElementById('updateFloorPermission_creators').checked];
      if (new_settings[2] === false && new_settings[3] === true) {
        M.toast({ html: 'Logic error in settings. 4rd cannot be checked while 3th is not checked', classes: 'rounded orange', displayLength: 2000 });
        await this.getFloorToUpdate();
      } else {
        const parser = new DOMParser();
        let xml_document = parser.parseFromString(this.updateFloor_data.data_to_update['xml_document'], 'text/xml');
        let permissions = xml_document.getElementsByTagName('setting');
        if (permissions[0].getAttribute('public').toLowerCase() !== String(new_settings[0]).toLowerCase())
          permissions[0].setAttribute('public', (new_settings[0] === true) ? 'True' : 'False')
        if (permissions[1].getAttribute('hidden').toLowerCase() !== String(new_settings[1]).toLowerCase())
          permissions[1].setAttribute('hidden', (new_settings[1] === true) ? 'True' : 'False')
        if (permissions[2].getAttribute('everybodyCanCreateRoom').toLowerCase() !== String(new_settings[2]).toLowerCase())
          permissions[2].setAttribute('everybodyCanCreateRoom', (new_settings[2] === true) ? 'True' : 'False')
        if (permissions[3].getAttribute('creatorCanDeleteRoom').toLowerCase() !== String(new_settings[3]).toLowerCase())
          permissions[3].setAttribute('creatorCanDeleteRoom', (new_settings[3] === true) ? 'True' : 'False')
        await this.$root.ADMIN_update_floor_xml_document(this.buildingName, this.updateFloor_data.selectedFloorToUpdate, xml_document).then(async (response) => {
          if (response[0] === true) {
            M.toast({html: 'Floor settings has been updated', classes: 'rounded green', displayLength: 2000});
            await this.getFloorToUpdate();
          } else
            M.toast({html: response[1], classes: 'rounded orange', displayLength: 2000});
        });
      }
    },
    async addAdmin() {
      if (this.adminBuilding_data.selectedNoAdmin === '')
        M.toast({ html: 'You have to select user', classes:'rounded orange', displayLength: 2000 });
      else {
        const parser = new DOMParser();
        let xml_document = parser.parseFromString(this.adminBuilding_data.xml_document, 'text/xml');
        let new_node = xml_document.createElement('admin');
        new_node.setAttribute('client_id', this.adminBuilding_data.selectedNoAdmin['id']);
        xml_document.getElementsByTagName('admin')[0].appendChild(new_node);
        await this.$root.ADMIN_update_building_xml_document(this.buildingName, xml_document).then(async (response) => {
          if (response[0] === true) {
            M.toast({html: 'Admin role has been added to user', classes: 'rounded green', displayLength: 2000});
            await this.changeView('');
            await this.changeView('adminBuilding');
          } else
            M.toast({html: response[1], classes: 'rounded orange', displayLength: 2000});
        });
      }
    },
    async removeAdmin() {
      if (this.adminBuilding_data.selectedAdmin === '')
        M.toast({ html: 'You have to select admin delete his role', classes:'rounded orange', displayLength: 2000 });
      else {
        const parser = new DOMParser();
        let xml_document = parser.parseFromString(this.adminBuilding_data.xml_document, 'text/xml');
        let elements = xml_document.getElementsByTagName('admin');
        let i = 0;
        for (; i < elements.length; i++) {
          if (Number(elements[i].getAttribute('client_id')) === this.adminBuilding_data.selectedAdmin['id'])
            break;
        }
        elements[i].parentNode.removeChild(elements[i]);
        await this.$root.ADMIN_update_building_xml_document(this.buildingName, xml_document).then(async (response) => {
          if (response[0] === true) {
            M.toast({html: 'Admin role has been deleted', classes: 'rounded green', displayLength: 2000});
            await this.changeView('');
            await this.changeView('adminBuilding');
          } else
            M.toast({html: response[1], classes: 'rounded orange', displayLength: 2000});
        });
      }
    }
  }
}
</script>

<style scoped>

</style>