module.exports = {
  'transpileDependencies': [
    'vuetify'
  ],
  'devServer': {
    'proxy': {
      '/auth/*': {
        'target': 'http://localhost:5000',
        'secure': false
      }
    }
  }
}
