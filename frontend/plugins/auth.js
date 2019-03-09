export default function ({ app }) {
    app.$auth.onError((error, name, endpoint) => {
        console.log("INI ERROR",error.response)
        console.log("NAMA", name)
    })
}