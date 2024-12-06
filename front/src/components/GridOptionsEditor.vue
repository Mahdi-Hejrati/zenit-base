<template>
    <q-dialog ref="dialogRef" @hide="DialogHide">
        <q-card style="width: 60%">
            <q-card-section>
              <div class="text-h6">تنظیمات نمایشی جدول {{ label }}</div>
              <div class="text-subtitle">نمایش ستون ها</div>
              <div class="row">
                  <div class="col-4" v-for="c in columns" v-bind:key="c.name">
                      <q-checkbox v-model="My.VisibleColumns" class="col" :val="c.name" :label="c.label" />
                  </div>
              </div>
            </q-card-section>
            <q-card-section>
              <div class="row">
                  <div class="col-4">
                      <q-select v-model="My.sortBy" label="مرتب سازی" 
                      :options="columns" option-value="name" option-label="label"
                      emit-value map-options/>
                  </div>
                  <div class="col-4 self-end">
                    <q-checkbox  v-model="My.descending" label="از انتها به ابتدا" />
                  </div>
                  <div class="col-4">
                      <q-select v-model="My.rowsPerPage" label="تعداد در صفحه" 
                      :options="[10,20,50,100]"/>
                  </div>
              </div>
            </q-card-section>
        </q-card>
    </q-dialog>
</template>
<script>

import { ref, onMounted, watch } from 'vue'
import { api } from 'boot/axios'
import ZenitUtils from '/src/ZenitUtils'
import _ from 'lodash'
import { useUserinfoStore } from 'stores/userinfo'
import { useDialogPluginComponent } from 'quasar'

export default {
  props: [
    "label", "columns", "pagination", "optionName"
  ],
  emits:[
    "update:pagination",
    ...useDialogPluginComponent.emits
  ],
  setup (props, { emit }) {
    const userinfo = useUserinfoStore()
    const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } = useDialogPluginComponent()
    
    const My = ref({
      VisibleColumns: [],
      sortBy: 'id',
      rowsPerPage: 10,
      descending: true
    })

    props.columns.forEach(element => {
      My.value.VisibleColumns.push(element.name)
    })

    const grid_options_name = props.optionName
    
    api.get('/options/' + grid_options_name)
    .then((response)=>{
      if(response.data) {
          const jd = JSON.parse(response.data)
          My.value = _.defaults(jd, My.value)
          emit("update:pagination", My.value)
        }
    })

    function DialogHide() {
      api.post('/options/' + grid_options_name, JSON.stringify(_.pick(
          My.value, ['VisibleColumns','sortBy','rowsPerPage','descending']))
      )
      emit("update:pagination", My.value)
      onDialogHide()
    }

    return {
    dialogRef,
    DialogHide,
    My,
    }
  }
}
</script>

