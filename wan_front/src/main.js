import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './plugins/element.js'
import './assets/css/global.css'
// import axios from 'axios'
import MyServerHtpp from './plugins/http.js'
Vue.use(MyServerHtpp);
Vue.config.productionTip = false;
new Vue({
  router,
  render: h => h(App)
}).$mount('#app');
