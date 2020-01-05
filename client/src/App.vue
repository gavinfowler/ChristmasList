<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <router-link to="/">
        <img alt="Vue logo" src="@/assets/logo-white.png" class="cursor" />
      </router-link>

      <v-spacer></v-spacer>
      <v-menu offset-y>
        <template v-slot:activator="{ on }">
          <v-btn dark v-on="on" icon>
            <v-icon>
              mdi-menu
            </v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item link to="/">
            <v-icon class="pr-2">mdi-home</v-icon>
            Home
          </v-list-item>
          <v-list-item link to="/family">
            <v-icon class="pr-2">mdi-account-group</v-icon>
            Family View
          </v-list-item>
          <v-list-item v-if="isAdmin" link to="/admin">
            <v-icon class="pr-2">mdi-shield-account</v-icon>
            Admin
          </v-list-item>
          <v-divider />
          <v-list-item @click="logout">
            <v-icon class="pr-2">mdi-logout</v-icon>
            Logout
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-content>
      <router-view />
    </v-content>
  </v-app>
</template>

<script>
export default {
  name: 'App',
  components: {},
  data: () => ({
    isAdmin: false
  }),
  mounted() {
    this.$http.interceptors.response.use(
      response => {
        return response
      },
      error => {
        if (error.response.status === 403) {
          this.$router.push('login')
        }
        return error
      }
    )
    this.$store.watch(
      state => state.user,
      () => {
        if (this.$store.state.user) {
          this.isAdmin = this.$store.state.user.is_admin
        } else {
          this.isAdmin = false
        }
      }
    )
  },
  methods: {
    test(msg) {
      console.log(msg)
    },
    logout() {
      this.$http
        .post('/auth/logout')
        .then(response => {
          this.$router.push('/login')
        })
        .catch(error => {
          console.log(error)
        })
    }
  }
}
</script>

<style>
.cursor {
  cursor: pointer;
}
</style>
