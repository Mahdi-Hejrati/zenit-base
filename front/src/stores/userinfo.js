import { defineStore } from 'pinia'
import { api } from 'boot/axios'
import _ from 'lodash'

export const useUserinfoStore = defineStore('userinfo', {
  state: () => ({
    whoami: {},    
  }),

  getters: {
    
  },

  actions: {

    checkUser(onFinish, force = false) {
      api.get('/whoami').then((response)=>{
        this.whoami = response.data
        if(typeof onFinish == "function")
          onFinish()
       })
    },
  }
})
