
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
      :columns="columns" optionName="groupgrid">
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
        name: 'group_name',
        sortable: true,
        label: 'group_name',
        align: 'left',
        field: row => row.group_name,
        format: val => `${val}`,
    },
    {
        name: 'group_poshtiban',
        sortable: true,
        label: 'group_poshtiban',
        align: 'left',
        field: row => row.group_poshtiban,
        format: val=>ZenitUtils.nano('user:{id}', val)
    },
    {
        name: 'group_start_date',
        sortable: true,
        label: 'group_start_date',
        align: 'left',
        field: row => row.group_start_date,
        format: val => `${val}`,
    },
    {
        name: 'group_start_page',
        sortable: true,
        label: 'group_start_page',
        align: 'left',
        field: row => row.group_start_page,
        format: val => `${val}`,
    },
    {
        name: 'group_assign_day',
        sortable: true,
        label: 'group_assign_day',
        align: 'left',
        field: row => row.group_assign_day,
        format: val => `${val}`,
    },
    {
        name: 'group_uc',
        sortable: true,
        label: 'group_uc',
        align: 'left',
        field: row => row.group_uc,
        format: val => `${val}`,
    },
    {
        name: 'group_type',
        sortable: true,
        label: 'group_type',
        align: 'left',
        field: row => row.group_type,
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

      const readUrl = '/group/read'
      loading.value = true

      let query_params = _.defaults(Thinginfo.query_params.group ?? {},
      {
        filter,
        page,
        pageSize: rowsPerPage,
        order_by: JSON.stringify([[sortBy ? sortBy : 'id', descending ? 'desc' : 'asc']]),
        load_1_group_poshtiban: true,
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

