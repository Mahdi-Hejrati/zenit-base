<template>
  <q-page class="flex flex-center" style="">
    <q-card>
      <q-card-section :horizontal="!$q.screen.lt.md">
        <q-card-section v-if="$q.screen.lt.md">
          <q-img src="logo.png" width="200px" style="margin: auto" spinner-color="green">
          </q-img>
        </q-card-section>
        <q-card-section>
          <q-card flat bordered>
            <q-card-section>
              <div class="row">
                <div class="col-xs-12 col-sm-12 q-pa-sm self-end ">
                <q-input v-model="user_login" 
                    label="نام کاربری" style="direction: ltr;">
                </q-input>
                </div>
                <div class="col-12">
                  <q-input v-model="user_pass" type="password" @keydown="zu.limitInput_en($event)"
                    :label="$t('رمز ورود')">
                  </q-input>
                </div>
              </div>
            </q-card-section>
            <q-card-actions>
              <div class="row full-width">
                <q-btn class="q-ma-sm" color="primary" @click="doLogin">{{ $t('ورود') }}</q-btn>
              </div>
            </q-card-actions>

            <q-card-section style="max-width:350px">
              <span style="color: red; max-width:350px; text-wrap: wrap;">{{ error_message }}</span>
            </q-card-section>

          </q-card>
        </q-card-section>
        <q-card-section v-if="!$q.screen.lt.md">
          <q-img src="logo.png" width="200px" spinner-color="green">
          </q-img>
        </q-card-section>

      </q-card-section>

    </q-card>
  </q-page>
</template>

<script>
import { ref } from 'vue';
import { defineComponent } from 'vue'
import { api } from 'boot/axios'
import { useRouter } from 'vue-router'
import { useUserinfoStore } from 'stores/userinfo'
import { useQuasar } from 'quasar';
import { useI18n } from 'vue-i18n';

export default defineComponent({
  setup() {
    const router = useRouter()
    const userinfo = useUserinfoStore()
    const $q = useQuasar()
    const { t } = useI18n()

    const user_pass = ref('')
    const error_message = ref('')
    const user_login = ref('')

    api.defaults.headers.common['Authorization'] = ''
    localStorage.setItem('login_token', null)

    const doLogin = () => {

      var loginFormData = new FormData();
      loginFormData.append('username', user_login.value);
      loginFormData.append('password', user_pass.value);
      loginFormData.append('grant_type', 'password');

      api.post("/login", loginFormData)
        .then(function (response) {
          var token = response.data.access_token
          api.defaults.headers.common['Authorization'] = 'Bearer ' + token
          localStorage.setItem('login_token', token)
          userinfo.checkUser(() => router.push('/'))
        })
        .catch((error) => {
          if (error.response) {

            if (error.response.status == 401) {
              error_message.value = "Invalid Login"
              return
            }

            error_message.value = JSON.stringify(response.response.data.detail)

            console.log('AxiosError', error.response.status, error.response.data, error.response.headers);
          } else if (error.request) {
            // The request was made but no response was received
            // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
            // http.ClientRequest in node.js
            console.log('AxiosRequestError', error.request);
          } else {
            // Something happened in setting up the request that triggered an Error
            console.log('AxiosErrorUknown', error.message);
          }
          console.log('AxiosErrorConfig', error.config);
        });
    }

    return {
      userinfo,
      user_pass,
      user_login,
      error_message,
      doLogin
    }
  }
})
</script>
