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
            Home
          </v-list-item>
          <v-list-item link to="/profile">
            Profile
          </v-list-item>
          <v-list-item
            v-for="(item, index) in items"
            :key="index"
            @click="test(item.title)"
          >
            {{ item.title }}
          </v-list-item>
          <v-divider />
          <v-list-item @click="logout">
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
    items: [
      { title: 'Click Me' },
      { title: 'Click Me' },
      { title: 'Click Me' },
      { title: 'Click Me 2' }
    ]
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
    if (this.$store.state.user === undefined) {
      this.$store.getUser()
    }
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
