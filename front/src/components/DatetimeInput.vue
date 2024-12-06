<template>
  <q-input v-bind="$attrs" v-model="Data" mask="####/##/##">
    <template v-slot:append v-if="!($attrs.readonly || $attrs.disable)">
      <q-icon name="event" class="cursor-pointer">
        <q-popup-proxy>
          <q-date v-model="Data" calendar="persian" today-btn>
            <div class="row items-center justify-end">
              <q-btn v-close-popup label="Close" color="primary" flat />
            </div>
          </q-date>
        </q-popup-proxy>
      </q-icon>
    </template>
  </q-input>
</template>

<script>
import { ref, watch } from 'vue'
import ZenitUtils from 'src/ZenitUtils'

export default {
  name: 'DatetimeInput',

  props: [
    "modelValue"
  ],
  emits: ["update:modelValue"],

  setup (props, { emit }) {
    const Data = ref("")

    watch(()=>props.modelValue, ()=>{
      if(props.modelValue){
        Data.value = ZenitUtils.date2sh(props.modelValue)
      }
    })

    watch(Data, ()=>{
      var d = ZenitUtils.sh2date(Data.value)
      emit('update:modelValue', d)
    })
    return {
      Data
    }
  }
}
</script>

