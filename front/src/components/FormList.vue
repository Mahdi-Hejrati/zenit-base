<template>
  <q-list bordered separator>
    <q-item>
      <q-item-section avatar>
        <q-btn class="q-mx-xs" @click="row_add()" round icon="add_circle_outline"></q-btn>
      </q-item-section>
      <q-item-label header>{{grid_title}}</q-item-label>
    </q-item>
    
    <q-item v-for="(row, ri) in rows" :key="row.idx" 
    :style="'background: ' + (ri % 2 ==0 ? 'transparent' : '#e8effa')">
      <q-item-section side top >
        <q-item-label caption>{{ row.idx }}</q-item-label>
        <q-btn class="q-mx-xs" @click="row_delete(row)" round icon="delete_outline"></q-btn>
      </q-item-section>
      <q-item-section>
        <MyForm v-model="rows[ri]"></MyForm>
      </q-item-section>
    </q-item>
  </q-list>
</template>

<script>

import { ref, onMounted, defineAsyncComponent } from 'vue'

var MyForm_name = ''

export default {
    name: 'FormList',
    components: { 
      MyForm: defineAsyncComponent(() => import('/src/components/' + MyForm_name + '.vue'))
    },
    props: [
        "modelValue",
        "grid_title",
        "form_name"
    ],
    emits: ["update:modelValue"],
    setup(props, { emit }) {
        MyForm_name = props.form_name

        const rows = ref([]);
        onMounted(() => {
            rows.value.splice(0, rows.value.length, ...props.modelValue);
            for (var i = 0; i < rows.value.length; i++) {
                rows.value[i].idx = i;
            }
        })

        const row_delete = (r) => {
            for (var i = 0; i < rows.value.length; i++) {
                if (rows.value[i].idx == r.idx) {
                    rows.value.splice(i, i + 1);
                }
            }
            emit("update:modelValue", rows.value);
        }

        const row_add = () =>{
          var last_ix = 0;
          for(var i=0; i<rows.value.length; i++){
            if(last_ix < rows.value[i].idx)
              last_ix = rows.value[i].idx
          }

          rows.value.push({
            idx: last_ix + 1
          })
          emit("update:modelValue", rows.value);
        }

        return {
            rows,
            row_delete,
            row_add
        };
    },
}
</script>

