// 定义全局参数
import Vue from 'vue'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App.vue'
import router from './router'
import i18n from './i18n/i18n'
import MathJax from './utils/MathJax'
// @表示src目录
import '@/assets/css/global.css'


Vue.prototype.MathJax = MathJax;
Vue.config.productionTip = false
Vue.use(ElementUI, { size: 'small'});

new Vue({
  router,
  i18n,
  render: h => h(App)
}).$mount('#app')


