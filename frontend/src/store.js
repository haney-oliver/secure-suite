import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex);
export default new Vuex.Store({
    plugins: [
        createPersistedState({
            storage: window.sessionStorage
        })
    ],
    state: {
        user: null,
        session_key: null
    },
    getters: {
        user(state) {
            return state.user
        },
        sessionKey(state) {
            return state.session_key
        }
    },
    mutations: {
        SET_USER_AND_SESSION(state, data) {
            state.user = data.user;
            state.session_key = data.session_key;
        }
    },
    actions: {
        setUserAndSession({ commit }, data) {
            commit("SET_USER_AND_SESSION", {
                user: data.user,
                session_key: data.session_key
            });
        },
        removeUserAndSession({ commit }) {
            commit("SET_USER_AND_SESSION", {
                user: null,
                session_key: null
            });
        }
    }
});
