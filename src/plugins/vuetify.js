import Vue from 'vue'
import Vuetify from 'vuetify/lib'

Vue.use(Vuetify)

export default new Vuetify({
  theme: {
    // dark: true
    themes: {
      light: {
        primary: '#235E6F',
        secondary: '#0F8A5F',
        accent: '#F5624D',
        error: '#CC231E',
        anchor: '#34A65F'
      }
    }
  }
})
