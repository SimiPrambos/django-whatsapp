const DefaultState = () => {
    return {
        setting: {}
    }
}

export const state = DefaultState()

export const actions = {
    GET_SETTING({ commit }) {
        this.$axios.get("setting/").then(response => {
            if (response.status === 200) {
                commit("SET_SETTING", response.data)
            }
        })
    },
    UPDATE_SETTING({ commit }, payload) {
        this.$axios.put("setting/", payload).then(response => {
            if (response.status === 200) {
                commit("SET_SETTING", response.data)
            }
        })
    }
}

export const mutations = {
    SET_SETTING(state, payload) {
        state.setting = payload
    }
}

export const getters = {
    setting(state) {
        return state.setting
    }
}