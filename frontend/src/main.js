import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import IdleVue from 'idle-vue'
import { EventBus } from './event-bus'

require('dotenv').config()

export const BACKEND_URI = process.env.BACKEND_URI

Vue.config.productionTip = false
Vue.use(IdleVue, {
    idleTime: 60000 * 10,
    eventEmitter: EventBus
});

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')
