module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  devServer: {
    proxy: "http://vocalotomo.herokuapp.com"
  }
}
