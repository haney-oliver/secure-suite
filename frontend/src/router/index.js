import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '@/components/views/HomeView.vue'
import LoginView from '@/components/views/LoginView.vue'
import DashboardView from '@/components/views/DashboardView.vue'
import RegisterView from '@/components/views/RegisterView.vue'
import VaultView from '@/components/views/VaultView.vue'

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
    },
    {
        path: '/register',
        name: 'RegisterView',
        component: RegisterView
    },
    {
        path: '/vault',
        name: 'VaultView',
        component: VaultView
    }
]

const router = new VueRouter({
    routes
})

export default router
