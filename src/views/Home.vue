<template>
  <div style="background-color: #dcdcdc; height: 100%">
    <div
      v-if="this.family === ''"
      style="width: 80%"
      class="text-center mx-auto"
    >
      <h1>Join a family</h1>
      <v-autocomplete
        label="Families"
        :items="allFamilies"
        item-text="name"
        item-value="key"
        v-model="familyKey"
      >
        <template v-slot:item="{ item }">
          {{ item.name }} (Key: {{ item.key }})
        </template>
      </v-autocomplete>
      <v-btn block color="primary" class="mt-4" @click="joinFamily">
        Join Family
      </v-btn>
    </div>
    <h1 class="text-center">View all families lists here</h1>
    <v-btn @click="test">
      Test
    </v-btn>
  </div>
</template>

<script>
export default {
  name: 'home',
  mounted() {
    this.getFamily()
    this.$http
      .get('family/getAllFamilies')
      .then(response => {
        if (response.data.families) {
          this.allFamilies = response.data.families
        }
      })
      .catch(error => console.error(error))
  },
  data: () => ({
    family: '',
    allFamilies: [],
    familyKey: 0
  }),
  methods: {
    getFamily() {
      console.log('getfamily')
      this.$http
        .get('family/getfamily')
        .then(response => {
          if (!response.data.error) {
            this.family = response.data.familyName
          }
        })
        .catch(error => console.error(error))
    },
    joinFamily() {
      console.log(this.familyKey)
      this.$http
        .post('/family/addfamily', { key: this.familyKey })
        .then(response => console.log(response))
        .catch(error => console.error(error))
    },
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
