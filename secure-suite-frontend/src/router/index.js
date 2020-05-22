import Vue from 'vue'
import Router from 'vue-router'
import LandingPage from '@/components/LandingPage'
import LoginForm from '@/components/LoginForm'
import RegisterForm from '@/components/RegisterForm'
import Vault from '@/components/Vault'
import Dashboard from '@/components/Dashboard'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'LandingPage',
      component: LandingPage
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginForm
    },
    {
      path: '/register',
      name: 'Register',
      component: RegisterForm
    },
    {
      path: '/vault/:userId',
      name: 'Vault',
      component: Vault
    },
    {
      path: '/dashboard/:userId',
      name: 'Dashboard',
      component: Dashboard
    }
  ]
})
