<template>
  <div>
    <h2 class="text-center">Families</h2>
    <v-btn class="mx-4" color="grey lighten-1" @click="getFamilies"
      ><v-icon class="pr-2">mdi-refresh</v-icon>Refresh</v-btn
    >
    <v-data-table
      :headers="familyHeaders"
      :items="families"
      :loading="loadingTable"
    >
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
        <v-icon small class="mr-2" @click="editFamilyHelper(item)">
          mdi-pencil
        </v-icon>
        <v-icon small @click="deleteFamilyHelper(item)">
          mdi-delete
        </v-icon>
      </template>
    </v-data-table>

    <!-- Dialogs -->

    <v-dialog max-width="500px" v-model="deleteFamilyDialog">
      <v-card>
        <v-card-title>
          Are you sure you want to delete this family?
        </v-card-title>
        <v-card-actions>
          <v-spacer />
          <v-btn color="warning" @click="deleteFamily"
            ><v-icon>mdi-delete</v-icon>Delete</v-btn
          >
          <v-btn color="grey lighten-1" @click="deleteFamilyDialog = false"
            >Cancel</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog max-width="650px" v-model="editFamilyDialog">
      <v-card>
        <v-card-title>
          Edit Family
        </v-card-title>
        <v-card-text>
          <v-text-field
            label="Name*"
            v-model="family.name"
            :rules="[rules.required]"
            outlined
          >
          </v-text-field>
          <v-text-field
            label="Creator"
            v-model="family.creator"
            outlined
            disabled
          />
          <v-text-field label="key" v-model="family.key" outlined disabled />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="success" @click="editFamily">Update</v-btn>
          <v-btn color="warning" @click="editFamilyDialog = false"
            >Cancel</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  name: 'AdminFamilies',
  mounted() {
    this.getFamilies()
  },
  data: () => ({
    loadingTable: false,
    families: [],
    currentDeleteFamily: {},
    deleteFamilyDialog: false,
    editFamilyDialog: false,
    // used for edit and create
    family: {
      name: '',
      creator: '',
      key: ''
    },
    rules: {
      required: value => !!value || 'Required'
    },
    familyHeaders: [
      { text: 'Name', value: 'name' },
      { text: 'Creator', value: 'creator' },
      { text: 'Key', value: 'key' },
      { text: 'Actions', value: 'action' }
    ]
  }),
  methods: {
    getFamilies() {
      this.loadingTable = true
      this.$http
        .get('/admin/families/get')
        .then(response => {
          this.families = response.data.families
          this.loadingTable = false
        })
        .catch(error => console.error(error))
    },
    editFamilyHelper(family) {
      this.family = family
      this.editFamilyDialog = true
    },
    editFamily() {
      this.editFamilyDialog = false
      this.$http
        .post('/admin/families/edit', this.family)
        .then(response => this.getFamilies())
        .catch(error => console.error(error))
    },
    deleteFamilyHelper(family) {
      this.currentDeleteFamily = family
      this.deleteFamilyDialog = true
    },
    deleteFamily() {
      this.deleteFamilyDialog = false
      this.$http
        .post('/admin/families/delete', { id: this.currentDeleteFamily.id })
        .then(response => this.getFamilies())
        .catch(error => console.error(error))
    }
  }
}
</script>

<style></style>
