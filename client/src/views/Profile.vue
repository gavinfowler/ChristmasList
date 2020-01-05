<template>
  <div class="px-12" style="background-color: #dcdcdc; height: 100%">
    <h1 class="text-center py-4">
      {{ this.$store.state.user.name }}'s Wish List
    </h1>
    <v-btn block color="primary" @click="showAddItem = !showAddItem">
      <div v-if="!showAddItem === true">Add an Item to Your List</div>
      <div v-else>Hide</div>
    </v-btn>
    <div v-if="showAddItem" class="pt-4">
      <v-card>
        <v-card-title>
          <h2>Add an item to your list</h2>
        </v-card-title>
        <v-card-text>
          <v-text-field
            label="Title*"
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
          <v-text-field label="Link to Item" v-model="item.item_url" outlined />
          <p>
            You can find a link to an image if you right click the image and
            select "Copy Link Location", once done, CTRL+v into the box below.
          </p>
          <v-text-field label="Image Url" v-model="item.img_url" outlined />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            block
            :disabled="this.item.title === ''"
            color="secondary"
            @click="submitItem"
            >Submit</v-btn
          >
        </v-card-actions>
      </v-card>
    </div>
    <div v-if="this.items.length > 0" class="pt-4">
      <div class="d-flex flex-wrap flex-row ">
        <v-card
          class="ma-4 d-flex flex-grow-1 flex-column item"
          v-for="item in items"
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
    <div v-else>
      <h2 class="text-center pt-8">No items have been entered</h2>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Profile',
  data: function() {
    return {
      dialog: false,
      showAddItem: false,
      name: '',
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
    if (this.$store.state.user) {
      this.name = this.$store.state.user
    } else {
      this.$store.watch(
        state => state.user,
        newVal => (this.name = newVal)
      )
    }
    this.getItems()
  },
  methods: {
    submitItem() {
      this.showAddItem = false
      this.$http.post('/post/addpost', this.item).then(response => {
        this.clear()
        this.getItems()
      })
    },
    getItems() {
      this.$http
        .get('/post/getposts')
        .then(response => {
          this.items = response.data.posts
        })
        .catch(error => console.error(error))
    },
    clear() {
      this.item = {
        title: '',
        notes: '',
        img_url: '',
        item_url: ''
      }
    },
    deleteItem(id) {
      this.$http
        .post('post/removepost', { id: id })
        .then(response => {
          console.log(response)
          this.getItems()
        })
        .catch(error => console.error(error))
    }
  },
  computed: {
    hasErrors() {
      return this.item.title !== ''
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
