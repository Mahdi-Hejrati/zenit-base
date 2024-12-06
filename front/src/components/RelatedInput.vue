<template>
    <q-input v-bind="$attrs" v-model="text" 
      :error="error" :error-message="errormessage">
      <template v-slot:append>
          <q-icon name="search" @click="opendg = true" >
          </q-icon>
        </template>
    </q-input>
    <q-dialog v-model="opendg">
      <q-card style="min-width: 60%">
        <q-card-section>
          <div class="text-h6">انتخاب {{$attrs.label}}</div>
        </q-card-section>
        <q-card-section class="q-pt-none">
          <component :is="grid_name" selection="single" v-model:selected="selected"></component>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="انتخاب" color="primary" @click="DoSelect" />
        </q-card-actions>
      </q-card>
      
    </q-dialog>
</template>

<script>
import { ref, onMounted, defineAsyncComponent, watch, computed } from 'vue'
import { api } from 'boot/axios'
import ZenitUtils from '/src/ZenitUtils'
import ProjectGrid from 'src/components/grids/ProjectGrid.vue'
import UserGrid from 'src/components/grids/UserGrid.vue'

export default {
  name: 'RelatedInput',

  props: [
    "modelValue",
    "related_to",
    "grid_name",
    "display_format"
  ],
  emits: ["update:modelValue"],

  setup (props, { emit }) {

    const opendg = ref(false)
    const selected = ref([])
    const related_to = props.related_to

    const error = ref(false)
    const errormessage = ref('')

    const text = ref('')
    const id = ref(0)

    const update_id = (id)=> {
      if(id){
        api.get('/' + related_to + '/' + id)
          .then((response)=>{
            text.value = props.display_format ? ZenitUtils.nano(props.display_format, response.data) : JSON.stringify(response.data)
            error.value = false
            errormessage.value = ""
          }).catch(()=>{
            error.value = true
            errormessage.value = "مقدار درست نیست"
          })
      } else {
        text.value = ''
        error.value = true
        errormessage.value = "انتخاب نشده است"
      }
    }

    onMounted(() => {
        id.value = props.modelValue
        update_id(id.value)
    });

    watch(()=>props.modelValue, ()=>{
        id.value = props.modelValue
        update_id(id.value)
    })

    const DoSelect = ()=>{
      id.value = (selected.value && selected.value.length) ? selected.value[0].id: null
      emit("update:modelValue", id.value)
      update_id(id.value)
      opendg.value = false
    }

    return {
      id,
      text,
      selected,
      opendg,
      DoSelect,
      error,
      errormessage
    };
  }
}
</script>

