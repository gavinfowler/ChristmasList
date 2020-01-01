<template>
  <div style="background-color: #dcdcdc; height: 100%">
    <div class="login-card-div">
      <v-card width="100%" class="login-card">
        <v-card-title>
          Login
        </v-card-title>
        <v-card-text>
          <v-text-field
            label="Username"
            :rules="[rules.required]"
            v-model="username"
            outlined
          >
            <v-icon slot="prepend">
              mdi-account
            </v-icon>
          </v-text-field>
          <v-text-field
            v-model="password"
            :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
            prepend-icon="mdi-lock"
            :rules="[rules.required]"
            :type="show ? 'text' : 'password'"
            name="password"
            label="Password"
            @click:append="show = !show"
            outlined
          ></v-text-field>
          <router-link to="/register" class="text-center">
            <h2>Register!</h2>
          </router-link>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <!-- <v-btn @click="submit" block> -->
          <v-btn
            @click="submit"
            :disabled="!(password !== '' && username !== '')"
            color="primary"
            block
          >
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
    show: false,
    rules: {
      required: value => !!value || 'Required'
    }
  }),
  methods: {
    submit() {
      this.$http
        .post('/auth/login', {
          username: this.username,
          password: this.password
        })
        .then(response => {
          if (response.data.authenticated) {
            this.$router.push('/')
          } else {
            this.error = response.data.error
          }
        })
        .catch(error => {
          console.error(error)
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
  width: 100%;
}
.login-card-div {
  width: 40%;
  margin: auto;
  padding-top: 5%;
}
@media only screen and (max-width: 1000px) {
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
