<template>
  <div style="background-color: #dcdcdc; height: 100%;" class="text-center">
    <h1>Admin Screen</h1>
    <v-tabs>
      <v-tab>
        Users
      </v-tab>
      <v-tab>
        Posts
      </v-tab>
      <v-tab>
        Families
      </v-tab>
      <v-tab-item>
        <h2>Users</h2>
        <v-data-table :headers="userHeaders" :items="users">
          <template v-slot:item.is_admin="{ item }">
            <v-icon color="green" v-if="item.is_admin">mdi-check</v-icon>
            <v-icon color="red" v-if="!item.is_admin">mdi-close</v-icon>
          </template>
          <template v-slot:item.action="{ item }">
            <v-icon small class="mr-2" @click="editUsers(item)">
              mdi-pencil
            </v-icon>
            <v-icon small @click="deleteUsers(item)">
              mdi-delete
            </v-icon>
          </template>
        </v-data-table>
      </v-tab-item>
      <v-tab-item>
        <h2>Posts</h2>
        <v-data-table :headers="postHeaders" :items="posts">
          <template v-slot:item.is_admin="{ item }">
            <v-icon color="green" v-if="item.is_admin">mdi-check</v-icon>
            <v-icon color="red" v-if="!item.is_admin">mdi-close</v-icon>
          </template>
          <template v-slot:item.action="{ item }">
            <v-icon small class="mr-2" @click="editUsers(item)">
              mdi-pencil
            </v-icon>
            <v-icon small @click="deleteUsers(item)">
              mdi-delete
            </v-icon>
          </template>
        </v-data-table>
      </v-tab-item>
      <v-tab-item>
        <h2>Families</h2>
        <v-data-table :headers="userHeaders" :items="users">
          <template v-slot:item.is_admin="{ item }">
            <v-icon color="green" v-if="item.is_admin">mdi-check</v-icon>
            <v-icon color="red" v-if="!item.is_admin">mdi-close</v-icon>
          </template>
          <template v-slot:item.action="{ item }">
            <v-icon small class="mr-2" @click="editUsers(item)">
              mdi-pencil
            </v-icon>
            <v-icon small @click="deleteUsers(item)">
              mdi-delete
            </v-icon>
          </template>
        </v-data-table>
      </v-tab-item>
    </v-tabs>
  </div>
</template>

<script>
export default {
  name: 'admin',
  mounted() {
    this.getFamilies()
    this.$http
      .get('/admin/users')
      .then(response => {
        this.users = response.data.users
        this.$http
          .get('/admin/posts')
          .then(response => {
            this.posts = response.data.posts
            console.log(this.posts)
            this.posts.forEach(post => {
              console.log(post.user_id)
              post.user = this.findUsername(post.user_id)
            })
            console.log(this.posts)
          })
          .catch(error => console.error(error))
      })
      .catch(error => console.error(error))
  },
  data: () => ({
    users: [],
    userHeaders: [
      { text: 'Username', value: 'username' },
      { text: 'Name', value: 'name' },
      { text: 'Email', value: 'email' },
      { text: 'Is Admin', value: 'is_admin' },
      { text: 'Family Id', value: 'family_id' },
      { text: 'Actions', value: 'action' }
    ],
    posts: [],
    postHeaders: [
      { text: 'Title', value: 'title' },
      { text: 'Owner', value: 'user' },
      { text: 'Notes', value: 'notes' },
      { text: 'Create Date', value: 'timestamp' },
      { text: 'Actions', value: 'action' }
    ],
    families: []
  }),
  methods: {
    getUsers() {
      console.log('getUsers')
      this.$http
        .get('/admin/users')
        .then(response => {
          console.log(response.data.users)
          this.users = response.data.users
        })
        .catch(error => console.error(error))
    },
    editUsers() {
      console.log('editUsers')
    },
    deleteUsers() {
      console.log('deleteUsers')
    },
    getPosts() {
      console.log('getPosts')
      this.$http
        .get('/admin/posts')
        .then(response => {
          this.posts = response.data.posts
          this.posts.forEach(post => {
            post.user = this.findUsername(post.user_id)
          })
          console.log(this.posts)
        })
        .catch(error => console.error(error))
    },
    findUsername(userId) {
      let username = ''
      this.users.forEach(user => {
        if (user.id === userId) {
          username = user.username
        }
      })
      return username
    },
    getFamilies() {
      console.log('getFamilies')
    }
  }
}
</script>

<style></style>
