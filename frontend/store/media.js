const DefaultState = () => {
    return {
        list: []
    }
}

export const state = DefaultState()

export const actions = {
    GET_MEDIA({ commit }) {
        this.$axios.get("media/").then(response => {
            if (response.status === 200) {
                commit("SET_MEDIA", response.data)
            }
        })
    },
    POST_MEDIA({ commit }, payload) {
        let media = new FormData();
        media.set("filename", payload.filename)
        media.set("filepath", payload.filepath)
        this.$axios.setHeader("Content-Type", "multipart/form-data")
        this.$axios.post("media/", media).then(response => {
            if (response.status === 201) {
                commit("ADD_MEDIA", response.data)
            }
        })
    },
    async DELETE_MEDIA({commit}, payload){
        await payload.map(media => {
            this.$axios.delete(`media/${media}/`).then(response => {
                if(response.status === 204){
                    commit("REMOVE_MEDIA", media)
                }
            })
        })
    }
}

export const mutations = {
    SET_MEDIA(state, media) {
        state.list = media
    },
    ADD_MEDIA(state, media) {
        state.list.push(media)
    },
    REMOVE_MEDIA(state, id){
        let index = state.list.findIndex(media => media.id === id)
        state.list.splice(index, 1)
    }
}

export const getters = {
    media(state) {
        return state.list
    }
}