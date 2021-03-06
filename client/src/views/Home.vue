<template>
  <div style="background-color: #dcdcdc; height: 100%;" class="px-8">
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
        outlined
      >
        <template v-slot:item="{ item }">
          {{ item.name }} (Key: {{ item.key }})
        </template>
        <template v-slot:no-data>
          <div class="pl-4">
            No families available, please create one
          </div>
        </template>
      </v-autocomplete>
      <v-btn block color="primary" class="mt-4" @click="joinFamily">
        Join Family
      </v-btn>
      <v-divider class="mt-8 mb-4" />
      <h1>Create a New Family</h1>
      <v-text-field outlined v-model="newFamily" label="New Family Name" />
      <v-btn block color="primary" class="mt-4" @click="createFamily">
        Create Family
      </v-btn>
    </div>
    <div v-else-if="family !== '' && family !== null">
      <h1 class="text-center">Family members lists</h1>
      <v-btn block color="primary" class="ma-4" @click="leaveFamily"
        >Leave Family</v-btn
      >
      <div v-for="set in familyPosts" :key="set['user']">
        <h2 class="text-center">{{ set['user'] }}'s Wish List</h2>
        <div class="d-flex flex-wrap flex-row">
          <v-card
            class="ma-4 d-flex flex-grow-1 flex-column item"
            v-for="item in set['posts']"
            :key="item.id"
          >
            <v-img
              :src="item.img_url"
              max-height="400"
              :contain="true"
              :alt="item.title"
              v-if="item.img_url"
            ></v-img>
            <div v-else class="text-center py-6 my-8">
              <v-icon x-large class="pb-4">
                mdi-camera-image
              </v-icon>
              <br />
              No image Available
            </div>
            <v-card-title> {{ item.title }} </v-card-title>
            <v-card-subtitle>
              {{ item.timestamp }}
            </v-card-subtitle>

            <v-card-text v-if="item.notes !== ''">
              {{ item.notes }}
            </v-card-text>
            <div class="flex-grow-1" />

            <v-card-actions>
              <v-btn :href="item.item_url" text v-if="item.item_url !== ''">
                View Item
              </v-btn>
              <v-spacer />
              <v-btn @click="deleteItem(item.id)" text color="error">
                Delete
              </v-btn>
            </v-card-actions>
          </v-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'home',
  mounted() {
    this.getFamily()
    this.getAllFamilies()
  },
  data: () => ({
    family: null,
    newFamily: '',
    allFamilies: [],
    familyKey: 0,
    familyUsers: [],
    familyPosts: []
  }),
  methods: {
    getFamily() {
      this.$http
        .get('family/getfamily')
        .then(response => {
          if (!response.data.error) {
            this.family = response.data.familyName
            this.getFamilyPosts()
          } else {
            this.family = ''
          }
        })
        .catch(error => console.error(error))
    },
    getAllFamilies() {
      this.$http
        .get('family/getAllFamilies')
        .then(response => {
          if (response.data.families) {
            this.allFamilies = response.data.families
          }
        })
        .catch(error => console.error(error))
    },
    getFamilyPosts() {
      this.$http
        .get('family/familyPosts')
        .then(response => {
          this.familyUsers = response.data.users
          this.familyPosts = response.data.posts
        })
        .catch(error => console.error(error))
    },
    joinFamily() {
      this.$http
        .post('/family/addfamily', { key: this.familyKey })
        .then(response => this.getFamily())
        .catch(error => console.error(error))
    },
    leaveFamily() {
      this.$http
        .delete('/family/removeFamily')
        .then(response => this.getFamily())
        .catch(error => console.error(error))
    },
    createFamily() {
      this.$http
        .post('/family/createfamily', { name: this.newFamily })
        .then(response => {
          this.getAllFamilies()
          this.familyKey = response.data.family.key
          this.joinFamily()
          this.newFamily = ''
        })
        .catch(error => console.error(error))
    },
    test() {
      this.$http
        .get('/test')
        .then(response => {
          console.log(response)
        })
        .catch(error => {
          console.error(error)
        })
    }
  }
}
</script>

<style scoped>
.item {
  min-width: 350px;
}
@media all and (max-width: 600px) {
  .item {
    min-width: 200px;
  }
}
</style>
