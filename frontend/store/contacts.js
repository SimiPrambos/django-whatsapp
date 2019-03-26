const DefaultState = () => {
    return {
        list: [],
        // category: []
    }
}

export const state = DefaultState()

export const actions = {
    async GET_CONTACTS({ commit }) {
        await this.$axios.get("contacts/").then(response => {
            if (response.status === 200) {
                commit("SET_CONTACTS", response.data)
            }
        })
    },
    POST_CONTACTS({ commit }, payload) {
        this.$axios.post("contacts/", payload, { progress: true }).then(response => {
            if (response.status === 201) {
                commit("ADD_CONTACTS", response.data)
            }
        })
    },
    async DELETE_CONTACTS({ commit }, payload) {
        await payload.map(contact => {
            this.$axios.delete(`contacts/${contact.id}/`).then(response => {
                if (response.status === 204) {
                    commit("REMOVE_CONTACTS", contact.id)
                }
            })
        })
    },
    IMPORT_CONTACTS({ commit }, payload) {
        this.$axios.post(`contacts/upload/`, payload).then(response => {
            if (response.status === 201) {
                commit("ADD_CONTACTS", response.data)
            }
        })
    }
}

export const mutations = {
    SET_CONTACTS(state, payload) {
        state.list = payload
    },
    ADD_CONTACTS(state, payload) {
        state.list = [...state.list, ...payload]
    },
    REMOVE_CONTACTS(state, id) {
        let index = state.list.findIndex(contact => contact.id === id)
        state.list.splice(index, 1)
    }
}

export const getters = {
    contacts(state) {
        return state.list
    },
    locations(state) {
        let locationlist = new Set();
        state.list.map(contact => {
            if (contact.location) {
                locationlist.add(contact.location)
            }
        })
        return [...locationlist]
    },
    professions(state) {
        let professionlist = new Set();
        state.list.map(contact => {
            if (contact.profession) {
                professionlist.add(contact.profession)
            }
        })
        return [...professionlist]
    }
}