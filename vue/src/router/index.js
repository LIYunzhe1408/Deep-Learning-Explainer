import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import side from '../views/SideMenu'
import Extraction from "@/views/Extraction";
import Initial from "@/views/Initial";

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'root',
    component: HomeView,
    redirect: '/home',
    children: [
      {path: 'home', name: 'Home', component: Initial},
      {path: 'extraction', name: 'Extraction', component: Extraction}
    ]
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
