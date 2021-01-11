<template>
  <div id="main" class="container white">
    <div class="row center-align">
      <b id="title">S e t t i n g s</b>
    </div>
      <form action="javascript:void(0)" id='updateProfileForm' @submit="submitForm('updateProfile')" class="container-fluid" style="margin: 5px 5px 5px 5px">
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
            <button @click="openModal('password')" type="button" class="btn blue">Change password</button>
          </div>
          <div class="input-field col">
            <button type="submit" class="btn blue darken-2">Update profile</button>
          </div>
          <div class="input-field col">
            <button @click="openModal('email')" type="button" class="btn blue">Change email</button>
          </div>
          </div>
      </form>
    <div id="passwordChangeModal" class="modal">
      <div class="modal-content">
        <h4 class="center-align">Change password</h4>
        <form @submit="submitForm('changePassword')" id='changePasswordForm' action="javascript:void(0)">
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
        <form @submit="submitForm('changeEmail')" id='changeEmailForm' action="javascript:void(0)">
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
import M from "materialize-css";

export default {
  name: 'profileSettings',
  methods: {
    openModal(which) {
      if (which === 'email')
        M.Modal.init(document.getElementById('emailChangeModal')).open();
      else if (which === 'password')
        M.Modal.init(document.getElementById('passwordChangeModal')).open();
    },
    async submitForm(form) {
      if (form === 'changeEmail') {
        const newMail = document.getElementById('profileSettingsNewEmail').value;
        const retypedMail = document.getElementById('profileSettingsNewRetypedEmail').value;
        if (newMail !== retypedMail)
          M.toast({ html: 'Emails do not match', classes: 'rounded orange', displayLength: 2000 });
        else {
          await this.$root.changeUserEmail(newMail).then(async (response) => {
            if (response[0] === true) {
              document.getElementById('changeEmailForm').reset();
              M.toast({html: 'Email address has been changed', classes: 'rounded green', displayLength: 2000});
              await this.$root.logoutUser().then((response) => {
                if (response[0] === true) {
                  M.toast({ html: 'You have been logged out', classes: 'rounded green', displayLength: 2000 });
                  this.$root.session_token = null;

                } else
                  M.toast({ html: response[1], classes: 'rounded orange', displayLength: 2000 });
              });
            }
          });
        }
      }
      else if (form === 'changePassword') {
        const newPassword = document.getElementById('profileSettingsNewPassword').value;
        const retypedPassword = document.getElementById('profileSettingsNewRetypedPassword').value;
        if (newPassword !== retypedPassword) {
          M.toast({ html: 'Passwords do not match', classes: 'rounded orange', displayLength: 2000 });
        }
        else {
          await this.$root.changeUserPassword(newPassword).then((response) => {
            if (response[0] === true) {
              M.toast({ html: 'Password has been changed', classes: 'rounded green', displayLength: 2000 });
              document.getElementById('changePasswordForm').reset();
              M.Modal.getInstance(document.getElementById('passwordChangeModal')).close();
            } else
              M.toast({ html: response[1], classes: 'rounded orange', displayLength: 2000 });
          });
        }
      }
      else if  (form === 'updateProfile') {
        const first_name = document.getElementById('profileSettingsFirstName').value;
        const second_name = document.getElementById('profileSettingsSecondName').value;
        const phone_number = document.getElementById('profileSettingsPhoneNumber').value.toString();
        const birth_date = document.getElementById('profileSettingsBirthDate').value;
        await this.$root.updateUserProfile(first_name, second_name, phone_number, birth_date).then((response) => {
          if (response[0] === true)
            M.toast({ html: 'Profile has been updated', classes: 'rounded green', displayLength: 2000 });
          else
            M.toast({ html: response[1], classes: 'rounded orange', displayLength: 2000 });
        });
      }
    },
  },
  async beforeMount() {
    await this.$root.getUserProfile().then((response) => {
      if (response[0] === true) {
        document.getElementById('profileSettingsFirstName').value = response[1][0]["first_name"];
        document.getElementById('profileSettingsSecondName').value = response[1][0]["second_name"];
        document.getElementById('profileSettingsPhoneNumber').value = response[1][0]["phone"];
        document.getElementById('profileSettingsBirthDate').value = response[1][0]["birth_date"];
        document.getElementById('profileSettingsEmail').value = response[1][0]["email"];
        document.getElementById('profileSettingsCreateDate').value = response[1][0]["created_date"]
      } else
        M.toast({ html: response[1], classes: 'rounded red', displayLength: 2000 });
    });
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