





<template>
    <q-dialog ref="dialog" @hide="onDialogHide">
      <q-card class="q-dialog-plugin">
        <q-card-section>
            <div class="text-h6 bg-primary text-white text-center">Edit user</div>
        </q-card-section>
        <div class="row">


          <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">

            <q-input v-model="Data.user_name" label="user_name"></q-input>

          </div>




          <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">

            <q-input v-model="Data.user_mobile" label="user_mobile"></q-input>

          </div>




          <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">

            <q-input v-model="Data.user_tel" label="user_tel"></q-input>

          </div>




          <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">

            <q-input v-model="Data.user_country" label="user_country"></q-input>

          </div>




          <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">

            <q-input v-model="Data.user_city" label="user_city"></q-input>

          </div>




          <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">

            <q-input v-model="Data.user_lang" label="user_lang"></q-input>

          </div>




          <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">

            <RelatedInput v-model="Data.user_group_id" related_to="group"
            label="user_group" 
            grid_name="GroupGrid" 
            display_format="group:{id}"></RelatedInput>

          </div>




          <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">

            <NumberInput v-model="Data.user_smshour" label="user_smshour" 
            justInt="true"></NumberInput>

          </div>




          <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">

            <q-input v-model="Data.user_access" label="user_access"></q-input>

          </div>




          <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">

            <q-checkbox v-model="Data.user_ack" label="user_ack"></q-checkbox>

          </div>




          <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">

            <q-checkbox v-model="Data.user_active" label="user_active"></q-checkbox>

          </div>




          <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">

            <DatetimeInput v-model="Data.user_bdate" label="user_bdate"></DatetimeInput>

          </div>




          <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">

            <NumberInput v-model="Data.user_money" label="user_money" 
            justInt="true"></NumberInput>

          </div>




          <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">

            <q-checkbox v-model="Data.user_iswomen" label="user_iswomen"></q-checkbox>

          </div>




          <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">

            <q-input v-model="Data.user_smslevel" label="user_smslevel"></q-input>

          </div>




          <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">

            <DatetimeInput v-model="Data.user_smsfinishdate" label="user_smsfinishdate"></DatetimeInput>

          </div>




          <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">

            <q-input v-model="Data.user_telegram_session" label="user_telegram_session"></q-input>

          </div>


        </div>
        <q-card-actions align="right">
        <q-btn color="primary" label="OK" @click="onOKClick" />
        <q-btn color="primary" label="Cancel" @click="onCancelClick" />
      </q-card-actions>
    </q-card>
  </q-dialog>
  <ErrorDisplay ref="error_display">
  </ErrorDisplay>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { api } from 'boot/axios'
import ErrorDisplay from 'components/ErrorDisplay.vue'
import RelatedInput from 'components/RelatedInput.vue'
import DatetimeInput from 'components/DatetimeInput.vue'
import NumberInput from 'components/NumberInput.vue'

export default {
  components:{
    ErrorDisplay,
    NumberInput, 
    RelatedInput, 
    DatetimeInput,   
  },
  props: {
    // ...your custom props
  },

  emits: [
    // REQUIRED
    'ok', 'hide'
  ],

  methods: {
    // following method is REQUIRED
    // (don't change its name --> "show")
    show (row) {
      this.Data = row
      this.$refs.dialog.show()
    },

    // following method is REQUIRED
    // (don't change its name --> "hide")
    hide () {
      this.$refs.dialog.hide()
    },

    onDialogHide () {
      // required to be emitted
      // when QDialog emits "hide" event
      this.$emit('hide')
    },

    onOKClick () {
      api.patch('/user/' + this.Data.id, this.Data)
      .then(response=>{
        var status = response.response?.status ?? response.status ?? 0
        if(status >= 400 && status < 500) {
          this.error_display.show(response.response.data.detail)
        }
        if(status >= 200 && status < 300) {
          this.$emit('ok')
          this.hide()
        }
      })

    },

    onCancelClick () {
      // we just need to hide the dialog
      this.hide()
    }
  },
  setup() {
      return {
          Data: ref({}),
          error_display: ref()
      }
  }
}
</script>

