const DefaultState = () => {
    return {
        list: []
    }
}

export const state = DefaultState()

export const actions = {
    RESET_STATE({ commit }) {
        commit('RESET_MESSAGES')
    },
    async GET_MESSAGES({ rootState, commit }) {
        this.$axios.setHeader("Api-Key", rootState.auth.user.api_key)
        let { data } = await this.$axios.get("messages/")
        commit("SET_MESSAGES", data)
    },
    POST_TEXT_MESSAGE({ rootState, commit }, payload) {
        this.$axios.setHeader("Api-Key", rootState.auth.user.api_key)
        this.$axios.post(`numbers/${payload.numberId}/chats/`, payload.messages, { progress: true })
            .then(response => {
                if (response.status === 201) {
                    commit("ADD_MESSAGES", response.data)
                }
            })
    },
    POST_MEDIA_MESSAGE({ rootState, commit }, payload) {
        this.$axios.setHeader("Api-Key", rootState.auth.user.api_key)
        this.$axios.post(`numbers/${payload.numberId}/media/`, payload.messages, { progress: true })
            .then(response => {
                if (response.status === 201) {
                    commit("ADD_MESSAGES", response.data)
                }
            })
    }
}

export const mutations = {
    RESET_MESSAGES(state) {
        Object.assign(state, DefaultState())
    },
    SET_MESSAGES(state, messages) {
        state.list = messages
    },
    ADD_MESSAGES(state, messages) {
        state.list.push(messages)
    }
}

export const getters = {
    messages(state) {
        return state.list
    },
    messageByNumber(state) {
        return (number, type) => state.list.filter(message => message.number === number && message.message_type === type)
    },
    messagesByType(state) {
        return (type) => state.list.filter(message => message.message_type === type)
    },
    messagesByStatus(state) {
        return (status) => state.list.filter(message => message.message_status === status)
    },
    messagesById(state) {
        return (id) => state.list.filter(message => message.id === id)
    }
}