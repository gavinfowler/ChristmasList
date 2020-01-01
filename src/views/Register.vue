<template>
  <div style="background-color: #dcdcdc; height: 100%">
    <div class="login-card-div">
      <v-card width="100%" class="login-card">
        <v-card-title>
          Register
        </v-card-title>
        <v-card-text>
          <v-text-field
            label="Username*"
            v-model="account.username"
            :rules="[rules.required]"
            outlined
          >
            <v-icon slot="prepend">
              mdi-account
            </v-icon>
          </v-text-field>
          <v-text-field
            label="Name*"
            v-model="account.name"
            :rules="[rules.required]"
            outlined
          >
            <v-icon slot="prepend">
              mdi-account-badge
            </v-icon>
          </v-text-field>
          <v-text-field
            label="Email*"
            :rules="[rules.required]"
            v-model="account.email"
            outlined
          >
            <v-icon slot="prepend">
              mdi-email
            </v-icon>
          </v-text-field>
          <v-text-field
            label="Password*"
            type="password"
            v-model="account.password"
            :rules="[rules.required]"
            outlined
          >
            <v-icon slot="prepend">
              mdi-lock
            </v-icon>
          </v-text-field>
          <v-text-field
            label="Check Password*"
            type="password"
            v-model="account.passwordCheck"
            :rules="[rules.required, rules.checkPass]"
            outlined
          >
            <v-icon slot="prepend">
              mdi-lock
            </v-icon>
          </v-text-field>
          <router-link to="/login" class="text-center">
            <h2>Login</h2>
          </router-link>
          <p class="error-text">
            {{ error }}
          </p>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="submit" color="primary" block :disabled="!hasErrors">
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
    error: '',
    rules: {
      required: value => !!value || 'Required'
    }
  }),
  computed: {
    hasErrors() {
      return (
        this.account.username !== '' &&
        this.account.name !== '' &&
        this.account.email !== '' &&
        this.account.password !== '' &&
        this.account.passwordCheck !== ''
      )
    }
  },
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
