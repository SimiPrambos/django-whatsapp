export const state = () => ({
    users: []
})

export const actions = {
    GET_USERS({ commit }) {
        this.$axios.get("users/").then(response => {
            if (response.status === 200) {
                commit("SET_USERS", response.data)
            }
        })
    },
    PUT_USERS_ACTIVE({ commit }, payload) {
        this.$axios.put(`users/${payload.id}/`, payload.data, { progress: true }).then(response => {
            if (response.status === 200) {
                commit("UPDATE_USERS_ACTIVE", response.data)
            }
        })
    },
    DELETE_USERS({ commit }, id) {
        this.$axios.delete(`users/${id}/`, { progress: true }).then(response => {
            if (response.status === 204) {
                commit("REMOVE_USERS", id)
            }
        })
    },
    PUT_EXPIRATION({commit}, payload){
        this.$axios.put(`users/${payload.id}/set_expiration/`, payload.data, { progress: true }).then(response => {
            if (response.status === 200) {
                console.log(response.data)
                commit("UPDATE_EXPIRATION", response.data)
            }
        })
    }
}

export const mutations = {
    SET_USERS(state, payload) {
        state.users = payload
    },
    UPDATE_USERS_ACTIVE(state, payload) {
        state.users.find(user => user.id === payload.id).is_active = payload.is_active
    },
    REMOVE_USERS(state, id){
        let index = state.users.findIndex(user => user.id === id)
        state.users.splice(index, 1)
    },
    UPDATE_EXPIRATION(state, payload){
        state.users.find(user => user.id === payload.id).api_expired = payload.api_expired
    }
}

export const getters = {
    users(state) {
        return state.users
    },
    usersActive(state) {
        return state.users.filter(user => user.is_active)
    },
    usersInactive(state) {
        return state.users.filter(user => !user.is_active)
    }
}