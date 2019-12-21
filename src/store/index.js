import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: {
      username: '',
      name: '',
      email: '',
      familyId: ''
    }
  },
  mutations: {
    setUser(state, response) {
      state.user = response.data.user
    }
  },
  actions: {
    getUser(context, callback) {
      axios.get('/auth/getuser').then(response => {
        context.commit('setUser', response)
      })
        .finally(() => {
          if (callback) {
            callback()
          }
        })
    }
  },
  modules: {
  }
})
