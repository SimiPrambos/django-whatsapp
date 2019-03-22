const DefaultState = () => {
    return {
        setting: {},
        // webhooks: []
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
    },
    // GET_WEBHOOKS({ commit }) {
    //     this.$axios.get("setting/webhook/").then(response => {
    //         if (response.status === 200) {
    //             commit("SET_WEBHOOKS", response.data)
    //         }
    //     })
    // },
}

export const mutations = {
    SET_SETTING(state, payload) {
        state.setting = payload
    },
    // SET_WEBHOOKS(state, payload) {
    //     state.webhooks = payload
    // }
}

export const getters = {
    setting(state) {
        return state.setting
    },
    // webhooks(state) {
    //     return state.webhooks
    // }
}