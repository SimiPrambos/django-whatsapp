const DefaultState = () => {
    return {
        list: [],
        friends: []
    }
}

export const state = DefaultState()

export const actions = {
    RESET_STATE({ commit }) {
        commit('RESET_MESSAGES')
    },
    GET_MESSAGES({ rootState, commit }) {
        this.$axios.setHeader("Api-Key", rootState.auth.user.api_key)
        this.$axios.get("messages/").then(response => {
            if (response.status === 200) {
                commit("SET_MESSAGES", response.data)
            }
        })
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
    },
    GET_FRIEND_MESSAGES({ commit }) {
        this.$axios.get("friend-messages/").then(response => {
            if (response.status === 200) {
                commit("SET_FRIEND_MESSAGES", response.data)
            }
        })
    },
    POST_FRIEND_MESSAGE({ commit }, payload) {
        this.$axios.post("friend-messages/", payload, { progress: true })
            .then(response => {
                if (response.status === 201) {
                    commit("ADD_FRIEND_MESSAGE", response.data)
                }
            })
    },
    PUT_FRIEND_MESSAGE({ commit }, payload) {
        this.$axios.put(`friend-messages/${payload.id}/`, payload.message, { progress: true })
            .then(response => {
                if (response.status === 200) {
                    commit("UPDATE_FRIEND_MESSAGE", response.data)
                }
            })
    },
    DELETE_FRIEND_MESSAGE({ commit }, id) {
        this.$axios.delete(`friend-messages/${id}/`, { progress: true })
            .then(response => {
                if (response.status === 204) {
                    commit("REMOVE_FRIEND_MESSAGE", id)
                }
            })
    },
    DELETE_MESSAGES({rootState, commit}, payload){
        this.$axios.setHeader("Api-Key", rootState.auth.user.api_key)
        this.$axios.delete(`numbers/${payload.number}/chats/${payload.id}/`, { progress: true })
            .then(response => {
                if (response.status === 204) {
                    commit("REMOVE_MESSAGES", payload.id)
                }
            })
    }
}

export const mutations = {
    RESET_MESSAGES(state) {
        Object.assign(state, DefaultState())
    },
    SET_MESSAGES(state, payload) {
        state.list = payload
    },
    ADD_MESSAGES(state, payload) {
        state.list.push(payload)
    },
    REMOVE_MESSAGES(state, id){
        let index = state.list.findIndex(message => message.id === id)
        state.list.splice(index, 1)
    },
    SET_FRIEND_MESSAGES(state, payload) {
        state.friends = payload
    },
    ADD_FRIEND_MESSAGE(state, payload) {
        state.friends.push(payload)
    },
    UPDATE_FRIEND_MESSAGE(state, payload) {
        state.friends.find(friend => friend.id === payload.id).message = payload.message
    },
    REMOVE_FRIEND_MESSAGE(state, id){
        let index = state.friends.findIndex(friend => friend.id === id)
        state.friends.splice(index, 1)
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
    },
    friendMessages(state) {
        return state.friends
    }
}