<template>
    <q-input v-bind="$attrs" v-model="Num" ></q-input>
</template>

<script>
import { ref, onMounted, watch, computed } from 'vue'


export default {
  name: 'NumberInput',

  props: [
    "modelValue",
    "justInt"
  ],
  emits: ["update:modelValue"],

  setup (props, { emit }) {

    const justInt = props.justInt

    const lv = ref(0)

    const Num = computed({
      get() {
        var lvval = lv.value

        if(isNaN(lvval)) 
          return  ''
        else {

          if(justInt)
          {
            lvval = Math.round(lvval)
          }

          var ret = lvval.toString()
          var d = ret.indexOf('.')
          var s = ''
          var f = ''

          if(d >=0 ){
            var s = ret.substring(0, d).replace(/\B(?=(\d{3})+(?!\d))/g, ",")
            var f = ret.substring(d+1, d+3)
            return s + '.' + f
          } else {
            return ret.replace(/\B(?=(\d{3})+(?!\d))/g, ",")
          }
        }
      },
      set(newValue) {
        lv.value = parseFloat(newValue.split(",").join(""))
      }
    })

    onMounted(() => (
        lv.value = !isNaN(props.modelValue) ? parseFloat(props.modelValue): Number.NaN
      )
    );

    watch(Num, () => {
      emit("update:modelValue", lv.value)
    });

    return {
      Num,
      lv
    };
  }
}
</script>

