<template>
  <div class="LoginView">
    <div class="container">
      <div class="row">
        <div class="xd col s12 z-depth-6 card-panel">
          <form action="javascript:void(0)" @submit="loginUser" id="loginForm">
            <div class="row"></div>
            <div class="row">
              <div class="input-field col s12">
                <i class="material-icons prefix">mail_outline</i>
                <input class="validate" id="loginEmail" type="email" required>
                <label for="loginEmail" data-error="wrong" data-success="right">Email</label>
              </div>
            </div>
            <div class="row">
              <div class="input-field col s12">
                <i class="material-icons prefix">lock_outline</i>
                <input id="loginPassword" type="password" required minlength="6">
                <label for="loginPassword">Password</label>
              </div>
            </div>
            <div class="row">
              <div class="input-field col s12">
                <button type="submit" class="btn waves-effect waves-light col s12">Login</button>
              </div>
            </div>
            <div class="row">
              <div class="input-field col s6 m6 l6">
                <p class="margin medium-small"><a @click="changeForm('toRegister')" href="javascript:void(0)">Register Now!</a></p>
              </div>
              <div class="input-field col s6 m6 l6">
                <p class="margin right-align medium-small"><a @click="changeForm('toPassword')" href="javascript:void(0)">Forgot password?</a></p>
              </div>
            </div>
          </form>
          <form action="javascript:void(0)" @submit="registerUser" id="registerForm">
            <div class="row"></div>
            <div class="row">
              <div class="input-field col s12">
                <i class="material-icons prefix">mail_outline</i>
                <input class="validate" id="registerEmail" type="email" required>
                <label for="registerEmail" data-error="wrong" data-success="right">Email</label>
              </div>
            </div>
            <div class="row">
              <div class="input-field col s12">
                <i class="material-icons prefix">lock_outline</i>
                <input id="registerPassword" type="password" required>
                <label for="registerPassword">Password</label>
              </div>
            </div>
            <div class="row">
              <div class="input-field col s12">
                <i class="material-icons prefix">lock_outline</i>
                <input id="retypePassword" type="password" required >
                <label for="retypePassword">Retype password</label>
              </div>
            </div>
            <div class="row">
              <div class="input-field col s12">
                <button type="button" @click="registerUser" class="btn waves-effect waves-light col s12">Register</button>
              </div>
            </div>
            <div class="row">
              <div class="input-field col s6 m6 l6">
                <p class="margin medium-small"><a @click="changeForm" href="javascript:void(0)">Have account? Login!</a></p>
              </div>
            </div>
          </form>
          <form action="javascript:void(0)" @submit=passwordReset id="passwordForm">
            <div class="row"></div>
            <div class="row">
              <div class="input-field col s12">
                <i class="material-icons prefix">mail_outline</i>
                <input id="passwordEmail" type="email" required>
                <label for="passwordEmail" data-error="wrong" data-success="right">Email</label>
              </div>
            </div>
            <div class="row">
              <div class="input-field col s12">
                <button type="submit" class="btn waves-effect waves-light col s12">Send Email</button>
              </div>
            </div>
            <div class="input-field col s6 m6 l6">
              <p class="margin left-align medium-small"><a @click="changeForm('toLogin')" href="javascript:void(0)">Back to login</a></p>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import M from 'materialize-css';

export default {
  name: 'LoginView',
  computed: {
    console: () => console,
  },
  mounted: function() {
    document.getElementById('loginForm').style.display = 'block';
    document.getElementById('registerForm').style.display = 'none';
    document.getElementById('passwordForm').style.display = 'none';
  },
  methods: {
    changeForm(where = '') {
      let loginForm = document.getElementById('loginForm');
      let registerForm = document.getElementById('registerForm');
      let passwordForm = document.getElementById('passwordForm');
      if (loginForm.style.display === 'block'  && where === 'toRegister') {
        loginForm.style.display = 'none'
        registerForm.style.display = 'block';
        passwordForm.style.display = 'none';
      } else if (loginForm.style.display === 'block'  && where === 'toPassword') {
        loginForm.style.display = 'none'
        registerForm.style.display = 'none';
        passwordForm.style.display = 'block';
      } else if (passwordForm.style.display === 'block' && where ==='toLogin') {
        loginForm.style.display = 'block'
        registerForm.style.display = 'none';
        passwordForm.style.display = 'none';
      } else if (registerForm.style.display === 'block') {
        loginForm.style.display = 'block'
        registerForm.style.display = 'none';
        passwordForm.style.display = 'none';
      } else if(passwordForm.style.display === 'block') {
        loginForm.style.display = 'block';
        registerForm.style.display = 'none';
        passwordForm.style.display = 'none';
      }
    },
    async registerUser() {
      let email = document.getElementById('registerEmail').value;
      let password = document.getElementById('registerPassword').value;
      let retypePassword = document.getElementById('retypePassword').value;
      if (password === retypePassword) {
        await this.$root.$data.fb.auth().setPersistence(this.$root.$data.fb.auth.Auth.Persistence.SESSION);
        await this.$root.$data.fb.auth().createUserWithEmailAndPassword(email, password).then(async () => {
          await axios.post(this.$root.$data.backend_url.concat('/client/create'), {
            uid: this.$root.$data.fb.auth().currentUser.uid
          }).then( async (response) => {
            if (response.data === 'User created') {
              M.toast({ html: 'You are logged in', classes: 'rounded green', displayLength: 2000 });
              this.$root.$data.logged = true;
              await axios.get(this.$root.$data.backend_url.concat('/client/', this.$root.$data.fb.auth().currentUser.uid, '/login')).then((response) => {
                if (response.data === 'Tokens assigned') {
                  M.toast({ html: 'Tokens assigned', classes: 'rounded green', displayLength: 2000 });
                } else {
                  M.toast({ html: 'Error while generating tokens', classes: 'rounded red', displayLength: 2000 });
                }
              });
            } else {
              await this.$root.$data.fb.auth().currentUser.delete();
              M.toast({ html: response.data, classes: 'rounded red', displayLength: 2000 });
            }
          });
        }).catch((error) => {
         M.toast({ html: error.message, classes: 'rounded red', displayLength: 2000 });
        });
      }
      else {
        M.toast({ html: 'Password fields do not match', classes: 'rounded orange', displayLength: 2000 });
      }
    },
    async loginUser() {
      let email = document.getElementById('loginEmail').value;
      let password = document.getElementById('loginPassword').value;
      await this.$root.$data.fb.auth().setPersistence(this.$root.$data.fb.auth.Auth.Persistence.SESSION);
      this.$root.$data.fb.auth().signInWithEmailAndPassword(email, password).then( async() => {
        M.toast({ html: 'You are logged in',classes: 'rounded green', displayLength: 2000 });
        this.$root.$data.logged = true;
        await axios.get(this.$root.$data.backend_url.concat('/client/', this.$root.$data.fb.auth().currentUser.uid, '/login')).then((response) => {
          if (response.data === 'Tokens assigned') {
            M.toast({ html: 'Tokens assigned', classes: 'rounded green', displayLength: 2000 });
          } else {
            M.toast({ html: 'Error while generating tokens ', classes: 'rounded red', displayLength: 2000});
          }
        });
      }).catch((error) => {
        M.toast({ html: error.message, classes: 'rounded red', displayLength: 2000 });
      });
    },
    async passwordReset() {
      const email = document.getElementById('passwordEmail').value;
      await this.$root.$data.fb.auth().sendPasswordResetEmail(email).then(() => {
        M.toast({ html: "Confirmation email has been sent." , classes: "rounded green", displayLength: 2000 });
      }).catch((error) => {
        M.toast({ html: error.message , classes: "rounded orange", displayLength: 2000 });
      });
      document.getElementById('passwordEmail').value = '';
    },
  },
}
</script>

<style scoped>
input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  margin: 0;
}
.LoginView {
  width: 600px;
  margin: auto;
  margin-top: 15%;
}
.xd {
  border: 5px outset #468499;
  box-shadow: 4px 4px 4px 4px #468199
}

</style>
