<template>
  <div>
    <h2 class="text-center">Posts</h2>
    <v-btn class="mx-4" color="grey lighten-1" @click="getPosts"
      ><v-icon class="pr-2">mdi-refresh</v-icon>Refresh</v-btn
    >
    <v-data-table :headers="postHeaders" :items="posts" :loading="loadingTable">
      <template v-slot:item.is_admin="{ item }">
        <v-icon color="green" v-if="item.is_admin">mdi-check</v-icon>
        <v-icon color="red" v-if="!item.is_admin">mdi-close</v-icon>
      </template>
      <template v-slot:item.link="{ item }">
        <v-btn
          v-if="item.item_url !== ''"
          link
          color="primary"
          :href="item.item_url"
          class="mr-3"
          ><v-icon class="pr-2">mdi-link</v-icon>Link</v-btn
        >
        <v-btn
          v-if="item.img_url !== ''"
          link
          :href="item.img_url"
          color="primary"
          ><v-icon class="pr-2">mdi-image</v-icon>Image</v-btn
        >
      </template>
      <template v-slot:item.action="{ item }">
        <v-icon small class="mr-2" @click="editPostHelper(item)">
          mdi-pencil
        </v-icon>
        <v-icon small @click="deletePostHelper(item)">
          mdi-delete
        </v-icon>
      </template>
    </v-data-table>

    <!-- Dialogs -->

    <v-dialog max-width="500px" v-model="deletePostDialog">
      <v-card>
        <v-card-title>
          Are you sure you want to delete this post?
        </v-card-title>
        <v-card-actions>
          <v-spacer />
          <v-btn color="warning" @click="deletePost"
            ><v-icon>mdi-delete</v-icon>Delete</v-btn
          >
          <v-btn color="grey lighten-1" @click="deletePostDialog = false"
            >Cancel</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog max-width="650px" v-model="editPostDialog">
      <v-card>
        <v-card-title>
          Edit Post
        </v-card-title>
        <v-card-text>
          <v-text-field
            label="title*"
            v-model="post.title"
            :rules="[rules.required]"
            outlined
          >
          </v-text-field>
          <v-textarea
            label="Notes"
            v-model="post.notes"
            name="notes"
            outlined
          />
          <v-text-field label="Link to Item" v-model="post.item_url" outlined />
          <v-text-field label="Link to Item" v-model="post.img_url" outlined />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="success" @click="editPost">Update</v-btn>
          <v-btn color="warning" @click="editPostDialog = false">Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  name: 'AdminPosts',
  mounted() {
    this.getPosts()
  },
  data: () => ({
    loadingTable: false,
    posts: [],
    currentDeletePost: {},
    deletePostDialog: false,
    editPostDialog: false,
    // used for edit and create
    post: {
      title: '',
      notes: '',
      item_url: '',
      img_url: ''
    },
    rules: {
      required: value => !!value || 'Required'
    },
    postHeaders: [
      { text: 'Title', value: 'title' },
      { text: 'Owner', value: 'username' },
      { text: 'Notes', value: 'notes', sortable: false },
      { text: 'Create Date', value: 'timestamp' },
      { text: 'Links', value: 'link', sortable: false },
      { text: 'Actions', value: 'action', sortable: false }
    ]
  }),
  methods: {
    getPosts() {
      this.loadingTable = true
      this.$http
        .get('/admin/posts/get')
        .then(response => {
          this.posts = response.data.posts
          this.loadingTable = false
        })
        .catch(error => console.error(error))
    },
    editPostHelper(post) {
      this.post = post
      this.editPostDialog = true
    },
    editPost() {
      this.editPostDialog = false
      this.$http
        .post('/admin/posts/edit', this.post)
        .then(response => this.getPosts())
        .catch(error => console.error(error))
    },
    deletePostHelper(post) {
      this.currentDeletePost = post
      this.deletePostDialog = true
    },
    deletePost() {
      this.deletePostDialog = false
      this.$http
        .post('/admin/posts/delete', { id: this.currentDeletePost.id })
        .then(response => this.getPosts())
        .catch(error => console.error(error))
    }
  }
}
</script>

<style></style>
