<template>
  <div>
    <h2 class="text-center">Users</h2>
    <v-btn class="mx-4" color="grey lighten-1" @click="getUsers"
      ><v-icon class="pr-2">mdi-refresh</v-icon>Refresh</v-btn
    >
    <v-btn class="mr-auto" color="primary" @click="createUserHelper"
      ><v-icon class="pr-2">mdi-account</v-icon>Add User</v-btn
    >
    <v-data-table :headers="userHeaders" :items="users" :loading="loadingTable">
      <template v-slot:item.is_admin="{ item }">
        <v-icon color="green" v-if="item.is_admin">mdi-check</v-icon>
        <v-icon color="red" v-if="!item.is_admin">mdi-close</v-icon>
      </template>
      <template v-slot:item.action="{ item }">
        <v-icon small class="mr-2" @click="editUserHelper(item)">
          mdi-pencil
        </v-icon>
        <v-icon small @click="deleteUserHelper(item)">
          mdi-delete
        </v-icon>
      </template>
    </v-data-table>

    <!-- Dialogs -->

    <v-dialog max-width="500px" v-model="deleteUserDialog">
      <v-card>
        <v-card-title>
          Are you sure you want to delete this user?
        </v-card-title>
        <v-card-actions>
          <v-spacer />
          <v-btn color="warning" @click="deleteUser"
            ><v-icon>mdi-delete</v-icon>Delete</v-btn
          >
          <v-btn color="grey lighten-1" @click="deleteUserDialog = false"
            >Cancel</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog max-width="650px" v-model="editUserDialog">
      <v-card>
        <v-card-title>
          Edit User
        </v-card-title>
        <v-card-text>
          <v-text-field
            label="Username*"
            v-model="account.username"
            :rules="[rules.required]"
            outlined
            disabled
          >
            <v-icon slot="prepend">
              mdi-account
            </v-icon>
          </v-text-field>
          <v-text-field
            label="Name*"
            v-model="account.name"
            :rules="[rules.required]"
            outlined
          >
            <v-icon slot="prepend">
              mdi-account-badge
            </v-icon>
          </v-text-field>
          <v-text-field
            label="Email*"
            :rules="[rules.required]"
            v-model="account.email"
            outlined
          >
            <v-icon slot="prepend">
              mdi-email
            </v-icon>
          </v-text-field>
          <v-checkbox
            dense
            prepend-icon="mdi-shield-account"
            color="primary"
            v-model="account.is_admin"
            label="Is Admin"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="success" @click="editUser">Update</v-btn>
          <v-btn color="warning" @click="editUserDialog = false">Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog max-width="650px" v-model="createUserDialog">
      <v-card>
        <v-card-title>
          Create User
        </v-card-title>
        <v-card-text>
          <v-text-field
            label="Username*"
            v-model="account.username"
            :rules="[rules.required]"
            outlined
          >
            <v-icon slot="prepend">
              mdi-account
            </v-icon>
          </v-text-field>
          <v-text-field
            label="Name*"
            v-model="account.name"
            :rules="[rules.required]"
            outlined
          >
            <v-icon slot="prepend">
              mdi-account-badge
            </v-icon>
          </v-text-field>
          <v-text-field
            label="Email*"
            :rules="[rules.required]"
            v-model="account.email"
            outlined
          >
            <v-icon slot="prepend">
              mdi-email
            </v-icon>
          </v-text-field>
          <v-text-field
            label="Password*"
            type="password"
            v-model="account.password"
            :rules="[rules.required]"
            outlined
          >
            <v-icon slot="prepend">
              mdi-lock
            </v-icon>
          </v-text-field>
          <v-checkbox
            dense
            prepend-icon="mdi-shield-account"
            color="primary"
            v-model="account.is_admin"
            label="Is Admin"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="success" @click="createUser">Create</v-btn>
          <v-btn color="warning" @click="createUserDialog = false"
            >Cancel</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  name: 'AdminUsers',
  mounted() {
    this.getUsers()
  },
  data: () => ({
    loadingTable: false,
    users: [],
    currentDeleteUser: {},
    deleteUserDialog: false,
    editUserDialog: false,
    createUserDialog: false,
    // used for edit and create
    account: {
      username: '',
      name: '',
      email: '',
      password: '',
      is_admin: false
    },
    rules: {
      required: value => !!value || 'Required'
    },
    userHeaders: [
      { text: 'Username', value: 'username' },
      { text: 'Name', value: 'name' },
      { text: 'Email', value: 'email' },
      { text: 'Is Admin', value: 'is_admin', sortable: false },
      { text: 'Family Id', value: 'family_id' },
      { text: 'Actions', value: 'action', sortable: false }
    ]
  }),
  methods: {
    getUsers() {
      this.loadingTable = true
      this.$http
        .get('/admin/users/get')
        .then(response => {
          this.users = response.data.users
          this.loadingTable = false
        })
        .catch(error => console.error(error))
    },
    editUserHelper(user) {
      this.account = user
      this.editUserDialog = true
    },
    editUser() {
      this.editUserDialog = false
      this.$http
        .post('/admin/users/edit', this.account)
        .then(response => this.getUsers())
        .catch(error => console.error(error))
    },
    createUserHelper() {
      this.account = {
        username: '',
        name: '',
        email: '',
        is_admin: false
      }
      this.createUserDialog = true
    },
    createUser() {
      this.createUserDialog = false
      this.$http
        .post('/admin/users/create', this.account)
        .then(response => {
          this.getUsers()
        })
        .catch(error => console.error(error))
    },
    deleteUserHelper(user) {
      this.currentDeleteUser = user
      this.deleteUserDialog = true
    },
    deleteUser() {
      this.deleteUserDialog = false
      this.$http
        .post('/admin/users/delete', { id: this.currentDeleteUser.id })
        .then(response => this.getUsers())
        .catch(error => console.error(error))
    }
  }
}
</script>

<style></style>
