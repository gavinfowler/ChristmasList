<template>
  <div class="px-12">
    <h2 class="text-center py-4">
      {{ this.$store.state.user.name }}'s Wish List
    </h2>
    <v-dialog v-model="dialog" width="700">
      <template v-slot:activator="{ on }">
        <v-btn block color="secondary" v-on="on">
          Add an Item to Your List
        </v-btn>
      </template>
      <v-card>
        <v-card-title>
          <div style="width: 100%;" class="d-flex justify-space-between">
            <h2>Test</h2>
            <v-spacer />
            <v-btn icon @click="dialog = false"
              ><v-icon>mdi-close</v-icon></v-btn
            >
          </div>
        </v-card-title>
        <v-card-text>
          Some dummy text
          <v-text-field
            label="Title"
            v-model="item.title"
            :rules="requiredRule"
            outlined
          />
          <v-textarea
            label="Notes"
            v-model="item.notes"
            name="notes"
            outlined
          />
          <v-text-field label="Link" v-model="item.item_url" outlined />
          <v-text-field label="Image Url" v-model="item.image_url" outlined />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="secondary" @click="submitItem">Submit</v-btn>
          <v-btn color="warning" @click="dialog = false">Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  name: 'Profile',
  data: function() {
    return {
      dialog: false,
      item: {
        title: '',
        notes: '',
        img_url: '',
        item_url: ''
      },
      requiredRule: [value => !!value || 'Required'],
      items: []
    }
  },
  mounted() {
    this.$http.get('/post/getposts').then(response => {
      this.items = response.data.posts
      console.log(this.items)
    })
  },
  methods: {
    submitItem() {
      this.dialog = false
      console.log(this.item)
      this.$http.post('/post/addpost', this.item).then(response => {
        console.log(response)
      })
    },
    clear() {
      this.item = {
        title: '',
        notes: '',
        img_url: '',
        item_url: ''
      }
    }
  }
}
</script>
