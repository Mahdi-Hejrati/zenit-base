<template>
    <q-page class="flex flex-center">
        <div class="row">
            <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">
            <q-input v-model="Data.user_name" label="نام"></q-input>
            </div>
            <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">
                <q-field label="جنسیت" stack-label>
                    <template v-slot:control>
                        <div class="row full-width">
                            <q-radio class="col-3" label="خانم" :val="true" v-model="Data.user_iswomen"></q-radio>
                            <q-radio class="col-3" label="آقا" :val="false" v-model="Data.user_iswomen"></q-radio>
                        </div>
                    </template>
                </q-field>
            </div>
            <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">
            <q-input v-model="Data.user_mobile" style="direction: ltr;" label="موبایل" readonly>
            </q-input>
            </div>
            <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">
                <q-input v-model="Data.user_tel" label="تلفن"></q-input>
            </div>

            <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">
            <q-input v-model="Data.user_country" label="کشور"></q-input>
            </div>
            <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">
            <q-input v-model="Data.user_city" label="شهر"></q-input>
            </div>
            <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">
            <q-select v-model="Data.user_lang" label="زبان"
                :options="[
                    {label:'فارسی', value:'Fa'},
                    {label:'English', value:'En'},
                    {label:'العربیه', value:'Ar'},
                ]" emit-value map-options></q-select>
            </div>

            <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">
            <q-select v-model="Data.user_smshour" label="ساعت پیام" 
                :options="[6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,20,22]"></q-select>
            </div>

            <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">
                <q-input readonly label="گروه شما"
                    :modelValue="z_.get(Data, 'user_group.group_name')">
                </q-input>
            </div>
            <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">
                <q-input readonly label="وضعیت فعالیت" 
                    :style="'background-color:' + (Data.user_active?'lightgreen':'pink')"
                    :modelValue="'مایل به قرائت ' + (Data.user_active?'هستم':'نیستم')">
                    <template v-slot:after>
                        <q-btn :icon="Data.user_active ? 'person_off':'person'" @click="change_active"></q-btn>
                    </template>
                </q-input>
            </div>
            <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">
            </div>
            <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">
                <q-btn color="primary" @click="update_profile">{{ $t('ثبت تغییرات') }}</q-btn>
            </div>
        </div>
    </q-page>
  </template>
  
  <script>
import { ref, defineComponent} from 'vue';
import { api } from 'boot/axios'
import { useQuasar, openURL } from 'quasar'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'
import { useUserinfoStore } from 'stores/userinfo'
import ZenitUtils from 'src/ZenitUtils';
import _ from 'lodash';
  
  export default defineComponent({
    name: 'user_profile',
    components: {
    },
    setup() {
        const route = useRoute()
        const $q = useQuasar()
        const { t } = useI18n()
        const userinfo = useUserinfoStore()
        const Data = ref({})
        
        userinfo.checkUser(()=>{
            api.get('/user/' + userinfo.whoami.id, {params:{
                load_group_user_group: true
            }}).then(response=>{
                Data.value = response.data
            })
        })

        function update_profile() {
            api.patch('/user/' + Data.value.id, null, {params:Data.value}).then(response=>{
                if(response.data && response.data.the_User) {
                    Data.value = response.data.the_User
                    $q.notify({
                        type: 'positive',
                        message: 'پروفایل کاربری بروزرسانی شد'
                    })
                }
            })
        }

        function change_active() {
            api.patch('/user/' + Data.value.id, null, {params:{
                user_active: !Data.value.user_active,
            }}).then(response=>{
                Data.value.user_active = response.data.the_User.user_active
            })
        }

        return {
            Data,
            userinfo,
            update_profile,
            change_active,
        };
    },
})
  </script>
  