import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);
export default new Vuex.Store({
    state: {
        user: null
    },
    getters: {
        user(state) {
            return state.user
        }
    },
    mutations: {
        SET_USER(state, data) {
            state.user = data;
        }
    },
    actions: {
        setUser({ commit }, user) {
            commit("SET_USER", {
                user: user
            });
        },
        removeUser({ commit }) {
            commit("SET_USER", {
                user: null
            });
        }
    }
});
