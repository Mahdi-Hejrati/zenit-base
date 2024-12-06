
<template>
  <q-page>
    <q-table 
      class="full-width q-pa-sm" 
      style="min-height: inherit !important; max-height: 1vh;" 
      flat bordered ref="tableRef" 
      :rows="rows"
      :columns="columns" 
      row-key="id" 
      v-model:pagination="pagination" 
      :loading="loading" 
      :filter="filter" 
      binary-state-sort
      @request="onRequest" 
      :visibleColumns="pagination.VisibleColumns">

      <template v-slot:top="props">
        <q-btn flat round icon="control_point_duplicate" 
        color="primary" @click="insert_row()"/>

        <div class="col-3 q-table__title">payment</div>

        <q-space />
        <q-input dense debounce="300" v-model="filter" placeholder="جستجو">
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>

        <q-btn flat round dense icon="tune" @click="GridOptionsView.show()" class="q-ml-md" />
        <q-btn flat round dense :icon="props.inFullscreen ? 'fullscreen_exit' : 'fullscreen'"
          @click="props.toggleFullscreen" class="q-ml-md" />
      </template>

      <template v-slot:body-cell-actions="props">
        <q-td :props="props" auto-width>
          <q-btn round dense flat icon="edit" size="sm" @click="edit_row(props.row)"></q-btn>
          <q-btn round dense flat icon="remove" size="sm" @click="delete_row_id = props.row.id;delete_form = true;"></q-btn>
          <q-btn round dense flat icon="source" size="sm" @click="display_row(props.row)"></q-btn>
        </q-td>
      </template>
    </q-table>
  </q-page>

  <GridOptionsEditor ref="GridOptionsView"
      :label="label" v-model:pagination="pagination" 
      :columns="columns" optionName="paymentpage">
  </GridOptionsEditor>
  <ObjectDisplay ref="object_display">
  </ObjectDisplay>
  <PaymentEdit ref="edit_form" @hide="refresh_grid()" @ok="refresh_grid()">
  </PaymentEdit>
  <PaymentInsert ref="insert_form" @hide="refresh_grid()" @ok="refresh_grid()">
  </PaymentInsert>
  <q-dialog v-model="delete_form">
    <q-card>
      <q-card-section class="row items-center">
        <q-avatar icon="delete" color="primary" text-color="white" />
        <span class="q-ml-sm">Delete Record?</span>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="Cancel" color="primary" v-close-popup />
        <q-btn flat label="Delete" color="red" @click="delete_row" v-close-popup/>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>

import { ref, onMounted, watch } from 'vue'
import { api } from 'boot/axios'
import ZenitUtils from '/src/ZenitUtils'
import { useUserinfoStore } from 'stores/userinfo'
import { useThinginfoStore } from 'stores/thinginfo'
import { useI18n } from "vue-i18n"
import GridOptionsEditor from 'src/components/GridOptionsEditor.vue'
import ObjectDisplay from 'src/components/ObjectDisplay.vue'
import PaymentEdit from 'src/components/forms/PaymentEdit.vue'
import PaymentInsert from 'src/components/forms/PaymentInsert.vue'
import _ from 'lodash'

const columns = [
    {
        name: 'id',
        sortable: true,
        label: 'ID',
        field: row => row.id,
        format: val => `${val}`,
    },
    {
        name: 'actions',
        label: 'عملیات'
    },
    {
        name: 'py_user',
        sortable: true,
        label: 'py_user',
        align: 'left',
        field: row => row.py_user,
        format: val=>ZenitUtils.nano('user:{id}', val)
    },
    {
        name: 'py_amount',
        sortable: true,
        label: 'py_amount',
        align: 'left',
        field: row => row.py_amount,
        format: val => `${val}`,
    },
    {
        name: 'py_desc',
        sortable: true,
        label: 'py_desc',
        align: 'left',
        field: row => row.py_desc,
        format: val => `${val}`,
    },
    {
        name: 'py_state',
        sortable: true,
        label: 'py_state',
        align: 'left',
        field: row => row.py_state,
        format: val => `${val}`,
    },
    {
        name: 'py_date',
        sortable: true,
        label: 'py_date',
        align: 'left',
        field: row => row.py_date,
        format: val => `${val}`,
    },
    {
        name: 'py_RefId',
        sortable: true,
        label: 'py_RefId',
        align: 'left',
        field: row => row.py_RefId,
        format: val => `${val}`,
    },
    {
        name: 'py_xpaypingrequestid',
        sortable: true,
        label: 'py_xpaypingrequestid',
        align: 'left',
        field: row => row.py_xpaypingrequestid,
        format: val => `${val}`,
    },
]

export default {
  props: [],
  components: {
    GridOptionsEditor,
    ObjectDisplay,
    PaymentEdit,
    PaymentInsert,
  },
  setup(props) {
    const { t } = useI18n()
    const userinfo = useUserinfoStore()
    const Thinginfo = useThinginfoStore()

    const tableRef = ref()
    const rows = ref([])
    const filter = ref('')
    const loading = ref(false)
    const pagination = ref({
      sortBy: 'id',
      descending: false,
      page: 1,
      rowsPerPage: 3,
      rowsNumber: 10
    })

    function onRequest(props) {
      const { page, rowsPerPage, sortBy, descending } = props.pagination
      const filter = props.filter

      const readUrl = '/payment/read'
      loading.value = true

      let query_params = _.defaults(Thinginfo.query_params.payment ?? {},
      {
        filter,
        page,
        pageSize: rowsPerPage,
        order_by: JSON.stringify([[sortBy ? sortBy : 'id', descending ? 'desc' : 'asc']]),
        load_1_py_user: true,
      })

      api.get(readUrl, {
        params: query_params
      })
      .then((response) => {
        rows.value.splice(0, rows.value.length, ...response.data.rows)
        pagination.value.rowsNumber = response.data.total

        pagination.value.page = response.data.page
        pagination.value.rowsPerPage = response.data.pageSize

        const ob = response.data.order_by[0];

        pagination.value.sortBy = ob[0]
        pagination.value.descending = (ob.length == 2) && ob[1] == 'desc'

        loading.value = false
      })
    }

    function refresh_grid() {
        tableRef.value.requestServerInteraction()
    }
    
    onMounted(() => {
      userinfo.checkUser(refresh_grid)
    })

    const object_display =ref()
    function display_row(row) {
      object_display.value.show(row)
    }

    const edit_form = ref()
    function edit_row(row) {
      edit_form.value.show(row)
    }

    const insert_form = ref()
    function insert_row(){
      insert_form.value.show()
    }

    const delete_form = ref(false)
    const delete_row_id = ref(0)
    function delete_row() {
      api.delete('/payment/' + delete_row_id.value)
      .then(response=>{
        refresh_grid()
      })
    }

    return {
      label: t('payment'),
      userinfo,
      refresh_grid,

      tableRef,
      filter,
      loading,
      pagination,
      columns,
      rows,
      onRequest,
      GridOptionsView: ref(),
      object_display,
      display_row,
      edit_form,
      edit_row,
      insert_form,
      insert_row,
      delete_row,
      delete_form,
      delete_row_id,
    }

  }
}
</script>

