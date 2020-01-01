<template>
  <div style="background-color: #dcdcdc; height: 100%">
    <h1 class="text-center">View all families lists here</h1>
    <v-btn @click="test">
      Test
    </v-btn>
  </div>
</template>

<script>
export default {
  name: 'home',
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
