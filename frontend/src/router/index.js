import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '@/components/views/HomeView.vue'
import LoginView from '@/components/views/LoginView.vue'
import DashboardView from '@/components/views/DashboardView.vue'

Vue.use(VueRouter)

  const routes = [
  {
    path: '/',
    name: 'HomeView',
    component: HomeView
  },
  {
    path: '/login',
    name: 'LoginView',
    component: LoginView
  },
  {
    path: '/dashboard',
    name: 'DashboardView',
    component: DashboardView
  }
]

const router = new VueRouter({
  routes
})

export default router
