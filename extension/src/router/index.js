import Vue from 'vue'
import VueRouter from 'vue-router'
import Vault from '@/components/Vault'
import Login from '@/components/Login'

Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/vault',
    name: 'Vault',
    component: Vault
  }
]

const router = new VueRouter({
  routes
})

export default router
