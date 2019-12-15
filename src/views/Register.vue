<template>
  <div style="background-color: #34A65F; height: 100%">
    <div class="login-card-div">
      <v-card width="100%" class="login-card">
        <v-card-title>
          Register
        </v-card-title>
        <v-card-text>
          <v-text-field placeholder="Username" v-model="account.username">
            <v-icon slot="prepend">
              mdi-account
            </v-icon>
          </v-text-field>
          <v-text-field placeholder="Name" v-model="account.name">
            <v-icon slot="prepend">
              mdi-account-badge
            </v-icon>
          </v-text-field>
          <v-text-field placeholder="Email" v-model="account.email">
            <v-icon slot="prepend">
              mdi-email
            </v-icon>
          </v-text-field>
          <v-text-field
            placeholder="Password"
            type="password"
            v-model="account.password"
          >
            <v-icon slot="prepend">
              mdi-lock
            </v-icon>
          </v-text-field>
          <v-text-field
            placeholder="Check Password"
            type="password"
            v-model="account.passwordCheck"
          >
            <v-icon slot="prepend">
              mdi-lock
            </v-icon>
          </v-text-field>
          <router-link to="/login" style="float: right">
            Login
          </router-link>
          <p class="error-text">
            {{ error }}
          </p>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="submit">
            <v-icon left>mdi-account-plus</v-icon>
            Register
          </v-btn>
        </v-card-actions>
      </v-card>
    </div>
  </div>
</template>
<script>
export default {
  name: 'Login',
  data: () => ({
    account: {
      username: '',
      name: '',
      email: '',
      password: '',
      passwordCheck: ''
    },
    error: ''
  }),
  methods: {
    submit() {
      this.error = ''
      if (this.account.password !== this.account.passwordCheck) {
        this.error = 'Passwords do not match'
        return
      }
      this.$http
        .post('/auth/register', {
          username: this.account.username,
          name: this.account.name,
          email: this.account.email,
          password: this.account.password
        })
        .then(response => {
          console.log(response)
          if (response.data.acknowledged) {
            this.$router.push('/login')
          } else {
            this.error = response.data.error
          }
        })
        .catch(e => {
          console.log(e)
        })
    }
  }
}
</script>
<style scoped>
.error-text {
  color: red;
  text-align: center;
}
.login-card {
  padding: auto;
}
.login-card-div {
  width: 60%;
  margin: auto;
  padding-top: 5%;
}
@media only screen and (max-width: 800px) {
  .login-card {
    width: 100%;
  }
  .login-card-div {
    width: 90%;
    margin: auto;
    padding-top: 20%;
  }
}
@media only screen and (max-width: 600px) {
  .login-card {
    width: 80%;
  }
  .login-card-div {
    width: 90%;
    margin: auto;
    padding-top: 20%;
  }
}
</style>
