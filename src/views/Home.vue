<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png" />
    <v-btn @click="test">
      Test
    </v-btn>
    <HelloWorld msg="Welcome to Your Vue.js App" />
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld'

export default {
  name: 'home',
  components: {
    HelloWorld
  },
  mounted() {},
  methods: {
    test() {
      this.$http
        .get('/test')
        .then(response => {
          console.log(response)
        })
        .catch(error => {
          console.log('error')
          console.log(error)
        })
    }
  }
}
</script>
