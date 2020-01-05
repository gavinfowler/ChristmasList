<template>
  <div style="background-color: #dcdcdc; height: 100%;">
    <h1 class="text-center">Admin</h1>
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
        <AdminUsers />
      </v-tab-item>
      <v-tab-item>
        <AdminPosts />
      </v-tab-item>
      <v-tab-item>
        <AdminFamilies />
      </v-tab-item>
    </v-tabs>
  </div>
</template>

<script>
import AdminUsers from '@/components/AdminUsers'
import AdminPosts from '@/components/AdminPosts'
import AdminFamilies from '@/components/AdminFamilies'

export default {
  name: 'admin',
  components: { AdminUsers, AdminPosts, AdminFamilies }
}
</script>

<style></style>
