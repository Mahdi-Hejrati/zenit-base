
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
      :columns="columns" optionName="smsgrid">
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
        name: 'user',
        sortable: true,
        label: 'user',
        align: 'left',
        field: row => row.user,
        format: val=>ZenitUtils.nano('user:{id}', val)
    },
    {
        name: 'sms_messageId',
        sortable: true,
        label: 'sms_messageId',
        align: 'left',
        field: row => row.sms_messageId,
        format: val => `${val}`,
    },
    {
        name: 'sms_moment',
        sortable: true,
        label: 'sms_moment',
        align: 'left',
        field: row => row.sms_moment,
        format: val => `${val}`,
    },
    {
        name: 'sms_receptor',
        sortable: true,
        label: 'sms_receptor',
        align: 'left',
        field: row => row.sms_receptor,
        format: val => `${val}`,
    },
    {
        name: 'sms_message',
        sortable: true,
        label: 'sms_message',
        align: 'left',
        field: row => row.sms_message,
        format: val => `${val}`,
    },
    {
        name: 'sms_status',
        sortable: true,
        label: 'sms_status',
        align: 'left',
        field: row => row.sms_status,
        format: val => `${val}`,
    },
    {
        name: 'sms_cost',
        sortable: true,
        label: 'sms_cost',
        align: 'left',
        field: row => row.sms_cost,
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

      const readUrl = '/sms/read'
      loading.value = true

      let query_params = _.defaults(Thinginfo.query_params.sms ?? {},
      {
        filter,
        page,
        pageSize: rowsPerPage,
        order_by: JSON.stringify([[sortBy ? sortBy : 'id', descending ? 'desc' : 'asc']]),
        load_1_user: true,
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

