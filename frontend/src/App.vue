<template>
  <AuthView v-if="session_token === null" />
  <AppView v-if="session_token !== null" />
</template>

<script>
import AuthView from "@/components/AuthView.vue";
import AppView from "@/components/AppView";
import axios from "axios";


export default {
  name: 'App',
  computed: {
    console: () => console
  },
  components: {
    AppView,
    AuthView,
  },
  methods: {
    async registerUser(email, password) {
      let result = [false, ''];
      await axios.post(this.backend_url.concat('/client/create'), {
        email: email,
        password: password
      }).then((response) => {
        if (response.status === 200)
          result[0] = true;
        result[1] = response.data;
      }).catch((error) => {
        result[1] = error.message;
      });
      return result;
    },
    async loginUser(email, password) {
      let result = [false, ''];
      await axios.post(this.backend_url.concat('/client/login'), {
        email: email,
        password: password
      }).then((response) => {
        if (response.status === 200)
          result[0] = true;
        result[1] = response.data;
      }).catch((error) => {
        result[1] = error.message;
      });
      return result;
    },
    async changeUserEmail(new_email) {
      let result = [false, ''];
      await axios.post(this.backend_url.concat('/client/', this.session_token, '/update/email'), {email: new_email}).then((response) => {
        if (response.status === 200)
          result[0] = true;
        result[1] = response.data;
      }).catch((error) => {
        result[1] = error.message;
      });
      return result;
    },
    async changeUserPassword(new_password) {
      let result = [false, ''];
      await axios.post(this.backend_url.concat('/client/', this.session_token, '/update/password'), {password: new_password}).then((response) => {
        if (response.status === 200)
          result[0] = true;
        result[1] = response.data;
      }).catch((error) => {
        result[1] = error.message;
      });
      return result;
    },
    async updateUserProfile(first_name, second_name, phone_number, birth_date) {
      let result = [false, ''];
      await axios.post(this.backend_url.concat('/client/', this.session_token, '/update/profile'), {
        first_name: first_name,
        second_name: second_name,
        phone_number: phone_number,
        birth_date: birth_date
      }).then((response) => {
        if (response.status === 200)
          result[0] = true;
        result[1] = response.data;
      }).catch((error) => {
        result[1] = error.message;
      });
      return result;
    },
    async logoutUser() {
      let result = [false, ''];
      await axios.put(this.backend_url.concat('/client/', this.session_token, '/logout')).then((response) => {
        if (response.status === 200)
          result[0] = true;
        result[1] = response.data;
      }).catch((error) => {
        result[1] = error.message;
      });
      return result;
    },
    async getUserProfile() {
      let result = [false, ''];
      await axios.get(this.backend_url.concat('/client/', this.session_token, '/get/profile')).then((response) => {
        if (response.status === 200)
          result[0] = true
        result[1] = response.data;
      }).catch((error) => {
        result[1] = error.message;
      });
      return result;
    },
    async sendPasswordResetEmail() {
      let result = [false, ''];
      let email = document.getElementById('passwordEmail').value;
      await axios.get(this.backend_url.concat('/mail/', email, '/send/link')).then((response) => {
        if (response.status === 200)
          result[0] = true;
        result[1] = response.data;
      }).catch((error) => {
        result[1] = error.message;
      });
      return result;
    },
  //  TODO:
    async getBuildingList() {
      let result = [false, ''];
      await axios.get(this.backend_url.concat('/application/', this.session_token, '/building/getlist')).then((response) => {
        if (response.status === 200)
          result[0] = true;
        result[1] = response.data;
      }).catch((error) => {
        result[1] = error.message;
      });
      return result;

    },
    async createBuilding(building_name) {
      let result = [false, ''];
      await axios.post(this.backend_url.concat('/application/', this.session_token, '/create/building'), {
        name: building_name,
      }).then((response) => {
        if (response.status === 200)
          result[0] = true;
        result[1] = response.data;
      }).catch((error) => {
        result[1] = error.message;
      });
      return result;
    },
    async getBuildingFloors(buildingName) {
      let result = [false, ''];
      await axios.get(this.backend_url.concat('/application/', this.session_token,'/building/', buildingName, '/get/floors')).then((response) => {
        if (response.status === 200)
          result[0] = true;
        result[1] = response.data;
      }).catch((error) => {
        result[1] = error.message;
      });
      return result;
    },
    ///
    async getFloorRooms(floorName, buildingName) {
      let result = [false, ''];
      await axios.get(this.backend_url.concat('/application/', this.session_token, '/building/', buildingName, '/floor/', floorName, '/get/rooms')).then((response) => {
        if (response.status === 200)
          result[0] = true;
        result[1] = response.data;
      }).catch((error) => {
        result[1] = error.message;
      });
      return result;
    },
    async addRoomToFloor(roomName, floorName, buildingName) {
      let result = [false, ''];
      await axios.post(this.backend_url.concat('/application/', this.session_token, '/building/', buildingName, '/floor/', floorName, '/create/room'), {
        roomName: roomName
      }).then((response) => {
        if (response.status === 200)
          result[0] = true;
        result[1] = response.data;
      }).catch((error) => {
        result[1] = error.message;
      })
      return result;
    },
    async getFilesInRoom(room_name, building_name, floor_name) {
      let result = [false, ''];
      await axios.get(this.backend_url.concat('/application/', this.session_token, '/building/', building_name, '/floor/', floor_name, '/room/', room_name, '/get/files')).then((response) => {
        if (response.status === 200)
          result[0] = true;
        result[1] = response.data;
      }).catch((error) => {
        result[1] = error.message;
      });
      return result;
    },
    ////
    async ADMIN_addFloorToBuilding(buildingName, floorName, floorPermissions) {
      let result = [false, ''];
      await axios.post(this.backend_url.concat('/application/admin/', this.session_token, '/building/', buildingName, '/create/floor'), {
        floorName: floorName,
        defaultPermissions: floorPermissions,
      }).then((response) => {
        if (response.status === 200)
          result[0] = true;
        result[1] = response.data;
      }).catch((error) => {
        result[1] = error.message;
      });
      return result;
    },
    async ADMIN_getAllFloorsForBuilding(buildingName) {
      let result = [false, ''];
      await axios.get(this.backend_url.concat('/application/admin/', this.session_token, '/building/', buildingName, '/get/floors')).then((response) => {
        if (response.status === 200)
          result[0] = true;
        result[1] = response.data;
      }).catch((error) => {
        result[1] = error.message;
      });
      return result;
    },
    async ADMIN_removeFloor(building_name, floor_name) {
      let result = [false, ''];
      await axios.put(this.backend_url.concat('/application/admin/', this.session_token, '/building/', building_name, '/floor/', floor_name, '/remove')).then((response) => {
        if (response.status === 200)
          result[0] = true;
        result[1] = response.data;
      }).catch((error) => {
        result[1] = error.message;
      });
      return result;
    },
    async ADMIN_getAllUsersForBuilding(building_name) {
      let result = [false, ''];
      await axios.get(this.backend_url.concat('/application/admin/', this.session_token, '/building/', building_name, '/get/users')).then((response) => {
        if (response.status === 200)
          result[0] = true;
        result[1] = response.data;
      }).catch((error) => {
        result[1] = error.message;
      });
      return result;
    },
    async ADMIN_removeUserFromBuilding(building_name, target_email) {
      let result = [false, ''];
      await axios.put(this.backend_url.concat('/application/admin/', this.session_token, '/building/', building_name, '/user/', target_email,'/remove')).then((response) => {
        if (response.status === 200)
          result[0] = true;
        result[1] = response.data;
      }).catch((error) => {
        result[1] = error.message;
      });
      return result;
    },
    async ADMIN_addUserToBuilding(building_name, target_email) {
      let result = [false, ''];
      await axios.post(this.backend_url.concat('/application/admin/', this.session_token, '/building/', building_name, '/user/add'), {
        target_email: target_email
      }).then((response) => {
        if (response.status === 200)
          result[0] = true;
        result[1] = response.data;
      }).catch((error) => {
        result[1] = error.message;
      });
      return result;
    },
    async ADMIN_getFullFloorData(building_name, floor_name) {
      let result = [false, ''];
      await axios.get(this.backend_url.concat('/application/admin/', this.session_token, '/building/', building_name, '/floor/', floor_name, '/get/data'),).then((response) => {
        if (response.status === 200)
          result[0] = true;
        result[1] = response.data;
      }).catch((error) => {
        result[1] = error.message;
      });
      return result;
    },
    async ADMIN_update_floor_xml_document(building_name, floor_name, xml_document) {
      let result = [false, ''];
      const serializer = new XMLSerializer();
      const xmlStr = serializer.serializeToString(xml_document);
      await axios.post(this.backend_url.concat('/application/admin/', this.session_token, '/building/', building_name, '/floor/', floor_name, '/update/xml'), {
        xml_document: xmlStr
      }).then((response) => {
        if (response.status === 200)
          result[0] = true;
        result[1] = response.data;
      }).catch((error) => {
        result[1] = error.message;
      });
      return result;
    }
  },
  data() {
    return {
      session_token: null,
      backend_url: 'http://127.0.0.1:5000',
    }
  },
}
</script>

<style>
body {
  background-image: url('assets/azure-6.jpg');
}
</style>
<!--https://dataroom-301309.ew.r.appspot.com-->