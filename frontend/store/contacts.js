const DefaultState = () => {
    return {
        list: [],
        groups: []
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
    async POST_CONTACTS({ rootState, commit }, payload) {
        this.$axios.setHeader("Api-Key", rootState.auth.user.api_key)
        await this.$axios.post("contacts/", payload).then(response => {
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
    async GET_GROUPS({ rootState, commit }) {
        this.$axios.setHeader("Api-Key", rootState.auth.user.api_key)
        await this.$axios.get("group/").then(response => {
            if (response.status === 200) {
                commit("SET_GROUPS", response.data)
            }
        })
    },
    async POST_GROUPS({ rootState, commit }, payload) {
        this.$axios.setHeader("Api-Key", rootState.auth.user.api_key)
        await this.$axios.post("group/", payload).then(response => {
            if (response.status === 201) {
                commit("ADD_GROUPS", response.data)
            }
        })
    },
}

export const mutations = {
    SET_CONTACTS(state, contacts) {
        state.list = contacts
    },
    ADD_CONTACTS(state, contacts) {
        state.list.push(contacts)
    },
    REMOVE_CONTACTS(state, id){
        let index = state.list.findIndex(contact => contact.id === id)
        state.list.splice(index, 1)
    },
    SET_GROUPS(state, groups) {
        state.groups = groups
    },
    ADD_GROUPS(state, groups){
        state.groups.push(groups)
    }
}

export const getters = {
    contacts(state) {
        return state.list
    },
    contactsByGroup(state){
        return (id) => state.list.filter(contact => contact.group === id)
    },
    groups(state) {
        return state.groups
    },
    groupsById(state) {
        return (id) => state.groups.find(group => group.id === id)
    }
}