
<template>
  <q-table
    v-bind="$attrs"
    class=""
    style="max-height: 500px"
    flat bordered
    ref="tableRef"
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
    <div class="col-3 q-table__title">{{ label }}</div>

    <q-space />

    <q-input borderless dense debounce="300" v-model="filter" placeholder="جستجو">
      <template v-slot:append>
        <q-icon name="search" />
      </template>
    </q-input>

    <q-btn
      flat round dense
      icon="tune"
      @click="GridOptionsView.show()"
      class="q-ml-md"
    />

    <q-btn
      flat round dense
      :icon="props.inFullscreen ? 'fullscreen_exit' : 'fullscreen'"
      @click="props.toggleFullscreen"
      class="q-ml-md"
    />
  </template>
  </q-table>

  <GridOptionsEditor ref="GridOptionsView"
      :label="label" v-model:pagination="pagination" 
      :columns="columns" optionName="paymentgrid">
  </GridOptionsEditor>
</template>

<script>

import { ref, onMounted, watch } from 'vue'
import { api } from 'boot/axios'
import ZenitUtils from '/src/ZenitUtils'
import { useUserinfoStore } from 'stores/userinfo'
import { useThinginfoStore } from 'stores/thinginfo'
import { useI18n } from "vue-i18n"
import GridOptionsEditor from 'src/components/GridOptionsEditor.vue'
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
  components: {
    GridOptionsEditor
  },
  props: [
    "label"
  ],
  setup (props) {
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

    return {
      refresh_grid,
      tableRef,
      filter,
      loading,
      pagination,
      columns,
      rows,
      onRequest,
      GridOptionsView: ref(),

    }

  }
}
</script>

