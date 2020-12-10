<template>
  <div id="main" class="container white" style="margin: 10px 10px 10px 10px;">
    <div class="row center-align">
      <b id="title">S e t t i n g s</b>
    </div>
      <form class="container-fluid" style="margin: 5px 5px 5px 5px">
        <div class="row">
          <div class="input-field col s6 left-align ">
            <input class="input" type="text" id="profileSettingsEmail" disabled/>
            <label for="profileSettingsEmail" class="active">Email address</label>
          </div>
          <div class="input-field col s6 right-align">
            <input class="input" type="date" id="profileSettingsCreateDate" disabled>
            <label for="profileSettingsCreateDate" class="active">Account created</label>
          </div>
        </div>
          <div class="row">
            <div class="input-field col s6 left-align">
              <input class="input" type="text" id="profileSettingsFirstName" minlength="3"/>
              <label for="profileSettingsFirstName" class="active">First name</label>
            </div>
            <div class="input-field col s6 right-align ">
              <input class="input" type="text" id="profileSettingsSecondName" minlength="2"/>
              <label for="profileSettingsSecondName" class="active">Second name</label>
            </div>
          </div>
        <div class="row">
          <div class="input-field col s6 left-align ">
            <input class="input" type="number" id="profileSettingsPhoneNumber" min="111111111" max="999999999"/>
            <label for="profileSettingsPhoneNumber" class="active">Phone number</label>
          </div>
          <div class="input-field col s6 right-align">
            <input class="input" type="date" id="profileSettingsBirthDate"/>
            <label for="profileSettingsBirthDate" class="active">Birthday date</label>
          </div>
        </div>
        <div class="row">
          <div class="input-field col">
            <button @click=openChangePasswordModal type="button" class="btn blue">Change password</button>
          </div>
          <div class="input-field col">
            <button @click=updateProfile type="button" class="btn blue darken-2">Update profile</button>
          </div>
          <div class="input-field col">
            <button @click=openChangeEmailModal type="button" class="btn blue">Change email</button>
          </div>
          </div>
      </form>
    <div id="passwordChangeModal" class="modal">
      <div class="modal-content">
        <h4 class="center-align">Change password</h4>
        <form @submit="changePassword" action="javascript:void(0)">
          <div class="input-field">
            <input type="password" id="profileSettingsNewPassword" minlength="6" required>
            <label for="profileSettingsNewPassword" class="active">New password</label>
          </div>
          <div class="input-field">
            <input type="password" id="profileSettingsNewRetypedPassword" minlength="6" required>
            <label for="profileSettingsNewRetypedPassword" class="active">Retype new password</label>
          </div>
          <div class="input-field center-align">
            <button type="submit" class="btn btn-blue">Submit</button>
          </div>
        </form>
      </div>
    </div>
    <div id="emailChangeModal" class="modal">
      <div class="modal-content">
        <h4 class="center-align">Change Email</h4>
        <form @submit="changeEmail" action="javascript:void(0)">
          <div class="input-field">
            <input type="email" id="profileSettingsNewEmail" required>
            <label for="profileSettingsNewEmail" class="active">New Email</label>
          </div>
          <div class="input-field">
            <input type="password" id="profileSettingsNewRetypedEmail" required>
            <label for="profileSettingsNewRetypedEmail" class="active">Retype new email</label>
          </div>
          <div class="input-field center-align">
            <p class="center-align">After submit and successfully email change you will be logged out</p>
            <button type="submit" class="btn btn-blue">Submit</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import M from 'materialize-css';

export default {
  name: 'profileSettings',
  methods: {
    updateData() {
      document.getElementById('profileSettingsEmail').value = this.$root.$data.fb.auth().currentUser.email;
      console.log(this.$parent.$data.currentClientInfo[4]);
      document.getElementById('profileSettingsCreateDate').value = this.$parent.$data.currentClientInfo[4];
      if (this.$parent.$data.currentClientInfo[1] != null) {
        document.getElementById('profileSettingsFirstName').value = this.$parent.$data.currentClientInfo[1];
      }
      if (this.$parent.$data.currentClientInfo[2] != null) {
        document.getElementById('profileSettingsSecondName').value = this.$parent.$data.currentClientInfo[2];
      }
      if (this.$parent.$data.currentClientInfo[3] != null) {
        document.getElementById('profileSettingsBirthDate').value = this.$parent.$data.currentClientInfo[3];
      }
      if (this.$parent.$data.currentClientInfo[5] != null) {
        document.getElementById('profileSettingsPhoneNumber').value = this.$parent.$data.currentClientInfo[5];
      }
    },
    async updateProfile() {
      const fn = document.getElementById('profileSettingsFirstName').value;
      const sn = document.getElementById('profileSettingsSecondName').value;
      const pn = document.getElementById('profileSettingsPhoneNumber').value;
      const bd = document.getElementById('profileSettingsBirthDate').value;
      if (pn.length !== 9) {
        M.toast({ html: 'Enter valid phone number', classes: 'rounded orange', displayLength: 2000 });
      }
      else {
        await axios.put(this.$root.$data.backend_url.concat('/client/', this.$root.$data.fb.auth().currentUser.uid.toString(), '/update'), {
          first_name: fn,
          second_name: sn,
          phone_number: pn,
          birth_date: bd
        }).then(async (response) => {
          if (response.data === 'OK') {
            M.toast({html: 'Profile updated', classes: 'rounded green', displayLength: 2000});
          }
        });
        await this.$parent.getClientInfo();
      }
    },
    openChangePasswordModal() {
      M.Modal.init(document.querySelectorAll('.modal'));
      const elem = document.getElementById('passwordChangeModal');
      const inst = M.Modal.getInstance(elem);
      inst.open();
    },
    openChangeEmailModal() {
      M.Modal.init(document.querySelectorAll('.modal'));
      const elem = document.getElementById('emailChangeModal');
      const inst = M.Modal.getInstance(elem);
      inst.open();
    },
    async changePassword() {
      const n = document.getElementById('profileSettingsNewPassword').value;
      const retyped = document.getElementById('profileSettingsNewRetypedPassword').value;
      if (n !== retyped) {
        M.toast({ html: 'Password fields do not match', classes: 'rounded orange', displayLength: 2000 });
      } else {
        await this.$root.$data.fb.auth().currentUser.updatePassword(n);
        M.toast({ html: 'Password updated', classes: "rounded green", displayLength: 2000 });
        const elem = document.getElementById('passwordChangeModal');
        const inst = M.Modal.getInstance(elem);
        inst.close();
      }
    },
    async changeEmail() {
      const n = document.getElementById('profileSettingsNewEmail').value;
      const retyped = document.getElementById('profileSettingsNewRetypedEmail').value;
      if (n !== retyped) {
        M.toast({ html: 'Email fields do not match', classes: 'rounded orange', displayLength: 2000 });
      } else {
        await this.$root.$data.fb.auth().currentUser.updateEmail(n);
        M.toast({ html: 'Email updated', classes: "rounded green", displayLength: 2000 });
        const elem = document.getElementById('emailChangeModal');
        const inst = M.Modal.getInstance(elem);
        inst.close();
        await this.$parent.logout();
      }
    }
  },
  mounted() {
    this.updateData();
  }
}
</script>

<style scoped>
h4 {
  font-size: 20px;
  font-family: Roboto,serif;
  color: blue;
  text-shadow: 1px 2px aqua;
}
#title {
  font-size: 20px;
  font-family: Roboto,serif;
  color: blue;
  text-shadow: 1px 2px aqua;
}
#main {
  border-right: 5px outset #468499;
  box-shadow: 4px 4px 4px 4px #468199
}
input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  margin: 0;
}
</style>