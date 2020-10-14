import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '@/components/views/HomeView'
import LoginView from '@/components/views/LoginView'
import DashboardView from '@/components/views/DashboardView'
import RegisterView from '@/components/views/RegisterView'
import VaultView from '@/components/views/VaultView'
import QuickstartView from '@/components/views/QuickstartView'

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
    }, 
    {
        path: '/quickstart',
        name: 'QuickstartView',
        component: QuickstartView
    }
]

const router = new VueRouter({
    routes
})

export default router
