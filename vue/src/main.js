// 定义全局参数
import Vue from 'vue'
import App from './App.vue'
import router from './router'

// @表示src目录
import '@/assets/css/global.css'

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
