import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './plugins/element.js'
import './assets/css/global.css'
import axios from 'axios'

Vue.config.productionTip = false
// var baseURLStr = window.g.ApiUrl
// axios.defaults.baseURL = baseURLStr

axios.defaults.baseURL = 'http://127.0.0.1:5555/api/v1/'

axios.defaults.headers.post['Content-Type'] = 'application/x-www-fromurlencodeed;charset=UTF-8'
Vue.prototype.$http = axios
new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
