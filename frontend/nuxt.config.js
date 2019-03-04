const VuetifyLoaderPlugin = require('vuetify-loader/lib/plugin')

module.exports = {
  mode: 'spa',

  /*
  ** Headers of the page
  */
  head: {
    title: 'WhatsPanel',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      {
        hid: 'description', name: 'description', content: 'Panel for easily manage whatsapp api'
      }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      {
        rel: 'stylesheet',
        href:
          'https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Material+Icons'
      }
    ],
  },

  /*
  ** Customize the progress-bar color
  */
  loading: { color: '#3adced', height: '2px' },

  /*
  ** Global CSS
  */
  css: [
    '~/assets/style/theme.styl',
    '~/assets/style/app.styl',
    'font-awesome/css/font-awesome.css',
    'roboto-fontface/css/roboto/roboto-fontface.css'
  ],

  /*
  ** Plugins to load before mounting the App
  */
  plugins: [
    '@/plugins/vuetify',
    '@/plugins/vee-validate',
    '@/plugins/vue-tel-input',
  ],

  /*
  ** Nuxt.js modules
  */
  modules: [
    '@nuxtjs/auth',
    '@nuxtjs/axios'
  ],

  /*
  ** Build configuration
  */
  build: {
    transpile: ['vuetify/lib'],
    plugins: [new VuetifyLoaderPlugin()],
    loaders: {
      stylus: {
        import: ["~assets/style/variables.styl"]
      }
    },

    /*
    ** You can extend webpack config here
    */
    extend(config, ctx) {

    }
  },

  axios: {
    baseURL: process.env.API_URL || '/api/'
  },

  auth: {
    rewriteRedirects: true,
    strategies: {
      local: {
        endpoints: {
          login: { url: 'auth/token/login/', method: 'post', propertyName: 'auth_token' },
          user: { url: 'auth/users/me/', method: 'get', propertyName: '' },
          logout: false,
        },
        tokenType: 'Token',
      }
    },
    redirect: {
      login: '/login',
      logout: '/login',
      home: '/dashboard',
    }
  }
}
