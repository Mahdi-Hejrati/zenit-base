<template>
    <q-page class="flex flex-center">
        <q-card class="q-ma-lx" style="max-width: 600px;">
            <q-card-section>

                <div class="row">
                    <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">
                    <q-input :disable="state == 1" v-model="Data.user_mobile" 
                        label="موبایل" style="direction: ltr;"
                        @keydown="zu.limitInput_int($event)">
                    </q-input>
                    </div>
                    <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">
                    <q-select :disable="state == 1" v-model="Data.mobile_prefix" 
                        style="direction: ltr;"
                        label="کد کشور" :options="userinfo.conutryCodes" emit-value map-options>
                    </q-select>
                    </div>
                    <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">
                    <q-input :disable="state == 1" v-model="Data.user_name" label="نام">
                    </q-input>
                    </div>

                    <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">
                    <q-select :disable="state == 1" v-model="Data.user_lang" label="زبان"
                        :options="[
                            {label:'فارسی', value:'Fa'},
                            {label:'English', value:'En'},
                            {label:'العربیه', value:'Ar'},
                        ]" emit-value map-options></q-select>
                    </div>

                    <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">
                    <q-input :disable="state == 1" v-model="Data.user_pass" label="رمز عبور"
                        type="password" @keydown="zu.limitInput_en($event)">
                    </q-input>
                    </div>
                    <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">
                    <q-input :disable="state == 1" v-model="Data.user_pass2" label="تکرار رمز عبور"
                        type="password" @keydown="zu.limitInput_en($event)">
                    </q-input>
                    </div>
                    <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">
                    <q-input :disable="state == 1" v-model="Data.user_country" label="کشور"></q-input>
                    </div>
                    <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">
                    <q-input :disable="state == 1" v-model="Data.user_city" label="شهر"></q-input>
                    </div>
                    <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">
                        <q-field :disable="state == 1" label="جنسیت" stack-label>
                            <template v-slot:control>
                                <div class="row full-width">
                                    <q-radio class="col-3" label="خانم" :val="true" v-model="Data.user_iswomen"></q-radio>
                                    <q-radio class="col-3" label="آقا" :val="false" v-model="Data.user_iswomen"></q-radio>
                                </div>
                            </template>
                        </q-field>
                    </div>
                    <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">
                        <q-input :disable="state == 1" v-model="Data.user_tel" label="تلفن"></q-input>
                    </div>

                    <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">
                    <q-select :disable="state == 1" v-model="Data.user_smshour" label="ساعت پیام" 
                        :options="[6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,20,22]"></q-select>
                    </div>

                    <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">
                        <q-input :style="`display: ${state == 1 ? 'inherit': 'none'};`" v-model="pincode" label="کد تایید"></q-input>
                    </div>

                    <div class="col-xs-6 col-sm-6 q-pa-sm self-end ">
                        <q-btn color="primary" @click="register_user">{{ (state == 1) ? $t('ثبت نام') : $t('دریافت کد تایید') }}</q-btn>
                    </div>

                    <div class="col-xs-6 col-sm-6 q-pa-sm self-end ">
                        <q-btn v-if="state == 1" color="primary" @click="state = 0">{{ $t('تغییر شماره همراه') }}</q-btn>
                    </div>
                </div>

            </q-card-section>
        </q-card>
    </q-page>
  </template>
  
  <script>
import { ref, defineComponent} from 'vue';
import { api } from 'boot/axios'
import { useQuasar, openURL } from 'quasar'
import { useI18n } from 'vue-i18n'
import { useRouter, useRoute } from 'vue-router'
import { useUserinfoStore } from 'stores/userinfo'
import ZenitUtils from 'src/ZenitUtils';
import _ from 'lodash'
  
  export default defineComponent({
    components: {},
    setup() {
        const route = useRoute()
        const router = useRouter()
        const $q = useQuasar()
        const { t } = useI18n()
        const userinfo = useUserinfoStore()
        const Data = ref({
            user_lang: 'Fa',
            mobile_prefix: '+98'
        })
        const pincode = ref('')
        const state = ref(0)
        const hash = ref('')

        function register_user() {
            if(state.value == 0) {
                let rg = /^\d{10}$/gm;

                if(!rg.test(Data.value.user_mobile)){
                    $q.notify({
                        type: 'negative',
                        message: 'شماره موبایل را به فرمت 9123456789 وارد کنید'
                    })
                    return
                }
                if(Data.value.user_pass != Data.value.user_pass2) {
                    $q.notify({
                        type: 'negative',
                        message: 'رمز ورود با تکرار آن مطابق نیست'
                    })
                    return
                }

                // request pincode
                api.get('/user/pincode', { params:{ user_login: Data.value.mobile_prefix + Data.value.user_mobile }})
                .then(response=>{
                    if(response && response.data && response.data.hash) {
                        hash.value = response.data.hash
                        state.value = 1
                        $q.notify({
                            type: 'warning',
                            message: t('لطفا کد ارسال شده را وارد نمایید')
                        })
                    }
                })
            } else if(state.value == 1) {
                api.post('/user/register', { the_User: Data.value }, { params: {
                    pincode: pincode.value,
                    user_login: Data.value.mobile_prefix + Data.value.user_mobile,
                    hash: hash.value,
                    user_pass: Data.value.user_pass,
                }}).then(response=>{
                    if(response && response.data && response.data.status_code == "200") {
                        var loginFormData = new FormData();
                        loginFormData.append('username', Data.value.mobile_prefix + Data.value.user_mobile);
                        loginFormData.append('password', Data.value.user_pass);
                        loginFormData.append('grant_type', 'password');

                        api.post("/login", loginFormData)
                        .then(function (response) {
                            var token = response.data.access_token
                            api.defaults.headers.common['Authorization'] = 'Bearer ' + token
                            localStorage.setItem('login_token', token)
                            router.push("/")                            
                        })
                    }
                })
            }
        }

        return {
            userinfo,
            Data,
            state,
            pincode,
            register_user,
        };
    },
})

</script>
  
