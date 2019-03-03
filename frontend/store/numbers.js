const DefaultState = () => {
    return {
        list: [],
        qrcodes: []
    }
}

export const state = DefaultState()

export const actions = {
    RESET_STATE({ commit }) {
        commit('RESET_NUMBERS')
    },
    GET_NUMBERS({ rootState, commit }) {
        this.$axios.setHeader("Api-Key", rootState.auth.user.api_key)
        this.$axios.get("numbers/").then(response => {
            if (response.status === 200) {
                commit("SET_NUMBERS", response.data)
            }
        })
    },
    async POST_NUMBERS({ rootState, commit }, payload) {
        this.$axios.setHeader("Api-Key", rootState.auth.user.api_key)
        await this.$axios.post("numbers/", payload).then(response => {
            if (response.status === 201) {
                commit("ADD_NUMBERS", response.data)
            }
        })
    },
    async DELETE_NUMBERS({ rootState, commit }, id) {
        this.$axios.setHeader("Api-Key", rootState.auth.user.api_key)
        await this.$axios.delete(`numbers/${id}/`).then(response => {
            if (response.status === 204) {
                commit("REMOVE_NUMBERS", id)
            }
        })
    },
    async SWITCH_NUMBER({ rootState, commit }, payload) {
        let status = payload.status === true ? "stop" : "start";
        this.$axios.setHeader("Api-Key", rootState.auth.user.api_key)
        await this.$axios.get(`numbers/${payload.id}/${status}/`, { progress: true }).then(response => {
            if (response.status == 200) {
                commit("UPDATE_STATUS_INSTANCE", { numberId: payload.id, status: response.data.running })
            }
        })
        await this.$axios.get(`numbers/${payload.id}/status/`).then(response => {
            if (response.status == 200) {
                commit("UPDATE_STATUS_LOGIN", { numberId: payload.id, status: response.data.is_logged_in })
            }
        })
    },
    SCAN_QRCODE({ rootState, commit }, id) {
        this.$axios.setHeader("Api-Key", rootState.auth.user.api_key)
        this.$axios.get(`numbers/${id}/login/`).then(response => {
            if (response.status === 200) {
                let qrcode = ""
                if (response.data.status === "isLoggedIn") {
                    commit("REMOVE_QRCODE", { numberId: id })
                    commit("UPDATE_STATUS_LOGIN", { numberId: id, status: true })
                } else {
                    qrcode = response.data.qrcode
                }
                commit("SET_QRCODE", { numberId: id, qrcode: qrcode })
            }
        })
    }
}

export const mutations = {
    RESET_NUMBERS(state) {
        Object.assign(state, DefaultState())
    },
    SET_NUMBERS(state, numbers) {
        state.list = numbers
    },
    ADD_NUMBERS(state, numbers) {
        state.list.push(numbers)
    },
    REMOVE_NUMBERS(state, id) {
        let index = state.list.findIndex(number => number.id === id)
        state.list.splice(index, 1)
    },
    UPDATE_STATUS_INSTANCE(state, payload) {
        state.list.find(number => number.id === payload.numberId).is_running = payload.status
    },
    UPDATE_STATUS_LOGIN(state, payload) {
        state.list.find(number => number.id === payload.numberId).is_logged_in = payload.status
    },
    SET_QRCODE(state, payload) {
        let number = state.list.find(number => number.id === payload.numberId)
        let source = { qrcode: payload.qrcode.length > 0 ? "data:image/png;base64," + payload.qrcode : payload.qrcode }
        Object.assign(number, source)
    },
    REMOVE_QRCODE(state, payload) {
        let number = state.list.find(number => number.id === payload.numberId)
        let source = { qrcode: "" }
        Object.assign(number, source)
    }
}

export const getters = {
    numbers(state) {
        return state.list
    },
    numbersById(state) {
        return (id) => state.list.find(number => number.id === id)
    },
    numbersIsRunning(state) {
        return state.list.filter(number => number.is_running === true)
    },
    numbersIsLoggedIn(state) {
        return state.list.filter(number => number.is_logged_in === true)
    },
    getQrCode(state) {
        return (id) => state.list.find(number => number.id === id).qrcode || ""
    }
}