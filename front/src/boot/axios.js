import { boot } from 'quasar/wrappers'
import axios from 'axios'

import { axios_cfg } from 'src/conf.js'

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)                  https://khatm-api.khedmatgozaran.com/docs
const api = axios.create(axios_cfg)

export default boot(({ app, router }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api

  app.config.globalProperties.$axios = axios
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  app.config.globalProperties.$api = api
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API


  api.interceptors.response.use(
    (response) => response, 
    (error) => {
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        if(error.response.status == 401){
          router.push('/login')
          return error
        }
        
        if(error.response.status >= 400 && error.response.status < 500){
          console.log('AxiosError', error.response.status, error.response.data, error.response.headers)
        }
      }
      return error;
    });


  if( localStorage.hasOwnProperty('login_token') )
    api.defaults.headers.common['Authorization'] = 'Bearer ' + localStorage['login_token'] 
})

export { api }
