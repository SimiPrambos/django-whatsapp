export default function ({ store, redirect }) {
    if (store.state.auth.user.was_expired) {
        redirect('/limitedaccess')
    }
}