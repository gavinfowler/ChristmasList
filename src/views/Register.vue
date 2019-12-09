<template>
  <div style="background-color: #34A65F; height: 100%">
    <div class="pt-12">
      <v-card width="30em" class="mx-auto">
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
</style>
