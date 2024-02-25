import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import side from '../views/SideMenu'
import Extraction from "@/views/Extraction";
import Home from "@/views/Home";
import Tree from "@/views/Tree";
import Explanation from "@/views/Explanation";

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'root',
    component: HomeView,
    redirect: '/home',
    children: [
      {path: 'home', name: 'Home', component: Home},
      {path: 'extraction', name: 'Extraction', component: Extraction},
      {path: 'tree', name: 'Tree', component: Tree},
      {path: 'explanation', name: 'explanation', component: Explanation}
    ]
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
