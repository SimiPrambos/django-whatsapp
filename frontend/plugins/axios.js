export default function ({ $axios, redirect }) {
    $axios.onError(error => {
      if(error.response.status === 403 && error.response.data.detail === 'Api Key was expired') {
        redirect('/limitedaccess')
      }
    })
  }