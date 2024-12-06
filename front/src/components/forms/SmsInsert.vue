
<template>
    <q-dialog ref="dialog" @hide="onDialogHide">
      <q-card class="q-dialog-plugin">
      <q-card-section>
          <div class="text-h6 bg-primary text-white text-center">Insert sms</div>
      </q-card-section>
        <div class="row">


          <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">

            <RelatedInput v-model="Data.user_id" related_to="user"
            label="user" 
            grid_name="UserGrid" 
            display_format="user:{id}"></RelatedInput>

          </div>




          <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">

            <q-input v-model="Data.sms_messageId" label="sms_messageId"></q-input>

          </div>




          <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">

            <q-input v-model="Data.sms_moment" label="sms_moment"></q-input>

          </div>




          <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">

            <q-input v-model="Data.sms_receptor" label="sms_receptor"></q-input>

          </div>




          <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">

            <q-input v-model="Data.sms_message" label="sms_message"></q-input>

          </div>




          <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">

            <q-checkbox v-model="Data.sms_status" label="sms_status"></q-checkbox>

          </div>




          <div class="col-xs-12 col-sm-6 q-pa-sm self-end ">

            <NumberInput v-model="Data.sms_cost" label="sms_cost" 
            justInt="true"></NumberInput>

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
    show () {
      this.Data = {}
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
      api.post('/sms', this.Data)
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

