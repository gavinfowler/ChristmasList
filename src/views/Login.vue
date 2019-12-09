<template>
  <div style="background-color: #34A65F; height: 100%">
    <div class="pt-12">
      <v-card width="30em" class="mx-auto">
        <v-card-title>
          Login
        </v-card-title>
        <v-card-text>
          <v-text-field placeholder="Username" v-model="username">
            <v-icon slot="prepend">
              mdi-account
            </v-icon>
          </v-text-field>
          <v-text-field
            placeholder="Password"
            type="password"
            v-model="password"
          >
            <v-icon slot="prepend">
              mdi-lock
            </v-icon>
          </v-text-field>
          <router-link to="/register" style="float: right">
            Register!
          </router-link>
          <p class="error-text">
            {{ error }}
          </p>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="submit">
            <v-icon left>mdi-login</v-icon>
            Login
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
    username: '',
    password: '',
    error: ''
  }),
  methods: {
    submit() {
      this.error = ''
      console.log(`username ${this.username}, password: ${this.password}`)
      this.$http
        .post('/auth/login', {
          username: this.username,
          password: this.password
        })
        .then(response => {
          console.log(response)
          if (response.data.authenticated) {
            this.$router.push('/')
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
