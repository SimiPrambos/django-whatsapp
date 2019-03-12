const DefaultState = () => {
    return {
        list: [],
        category: []
    }
}

export const state = DefaultState()

export const actions = {
    async GET_CONTACTS({ rootState, commit }) {
        this.$axios.setHeader("Api-Key", rootState.auth.user.api_key)
        await this.$axios.get("contacts/").then(response => {
            if (response.status === 200) {
                commit("SET_CONTACTS", response.data)
            }
        })
    },
    POST_CONTACTS({ rootState, commit }, payload) {
        this.$axios.setHeader("Api-Key", rootState.auth.user.api_key)
        this.$axios.post("contacts/", payload, { progress: true }).then(response => {
            if (response.status === 201) {
                commit("ADD_CONTACTS", response.data)
            }
        })
    },
    async DELETE_CONTACTS({ rootState, commit }, payload) {
        await payload.map(contact => {
            this.$axios.setHeader("Api-Key", rootState.auth.user.api_key)
            this.$axios.delete(`contacts/${contact.id}/`).then(response => {
                if (response.status === 204) {
                    commit("REMOVE_CONTACTS", contact.id)
                }
            })
        })
    },
    async GET_CATEGORY({ rootState, commit }) {
        this.$axios.setHeader("Api-Key", rootState.auth.user.api_key)
        await this.$axios.get("category/").then(response => {
            if (response.status === 200) {
                commit("SET_CATEGORY", response.data)
            }
        })
    },
    POST_CATEGORY({ rootState, commit }, payload) {
        this.$axios.setHeader("Api-Key", rootState.auth.user.api_key)
        this.$axios.post("category/", payload, { progress: true }).then(response => {
            if (response.status === 201) {
                commit("ADD_CATEGORY", response.data)
            }
        })
    },
}

export const mutations = {
    SET_CONTACTS(state, payload) {
        state.list = payload
    },
    ADD_CONTACTS(state, payload) {
        state.list.push(payload)
    },
    REMOVE_CONTACTS(state, id) {
        let index = state.list.findIndex(contact => contact.id === id)
        state.list.splice(index, 1)
    },
    SET_CATEGORY(state, payload) {
        state.category = payload
    },
    ADD_CATEGORY(state, payload) {
        state.category.push(payload)
    }
}

export const getters = {
    contacts(state) {
        return state.list
    },
    contactsByCategory(state) {
        return (id) => state.list.filter(contact => contact.category.includes(id) === true)
    },
    category(state) {
        return state.category
    },
    categoryById(state) {
        return (id) => state.category.find(cat => cat.id === id)
    }
}