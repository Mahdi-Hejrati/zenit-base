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
      :columns="columns" optionName="usergrid">
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
        name: 'user_name',
        sortable: true,
        label: 'user_name',
        align: 'left',
        field: row => row.user_name,
        format: val => `${val}`,
    },
    {
        name: 'user_mobile',
        sortable: true,
        label: 'user_mobile',
        align: 'left',
        field: row => row.user_mobile,
        format: val => `${val}`,
    },
    {
        name: 'user_tel',
        sortable: true,
        label: 'user_tel',
        align: 'left',
        field: row => row.user_tel,
        format: val => `${val}`,
    },
    {
        name: 'user_country',
        sortable: true,
        label: 'user_country',
        align: 'left',
        field: row => row.user_country,
        format: val => `${val}`,
    },
    {
        name: 'user_city',
        sortable: true,
        label: 'user_city',
        align: 'left',
        field: row => row.user_city,
        format: val => `${val}`,
    },
    {
        name: 'user_lang',
        sortable: true,
        label: 'user_lang',
        align: 'left',
        field: row => row.user_lang,
        format: val => `${val}`,
    },
    {
        name: 'user_group',
        sortable: true,
        label: 'user_group',
        align: 'left',
        field: row => row.user_group,
        format: val=>ZenitUtils.nano('group:{id}', val)
    },
    {
        name: 'user_smshour',
        sortable: true,
        label: 'user_smshour',
        align: 'left',
        field: row => row.user_smshour,
        format: val => `${val}`,
    },
    {
        name: 'user_access',
        sortable: true,
        label: 'user_access',
        align: 'left',
        field: row => row.user_access,
        format: val => `${val}`,
    },
    {
        name: 'user_ack',
        sortable: true,
        label: 'user_ack',
        align: 'left',
        field: row => row.user_ack,
        format: val => `${val}`,
    },
    {
        name: 'user_active',
        sortable: true,
        label: 'user_active',
        align: 'left',
        field: row => row.user_active,
        format: val => `${val}`,
    },
    {
        name: 'user_bdate',
        sortable: true,
        label: 'user_bdate',
        align: 'left',
        field: row => row.user_bdate,
        format: val => `${val}`,
    },
    {
        name: 'user_money',
        sortable: true,
        label: 'user_money',
        align: 'left',
        field: row => row.user_money,
        format: val => `${val}`,
    },
    {
        name: 'user_iswomen',
        sortable: true,
        label: 'user_iswomen',
        align: 'left',
        field: row => row.user_iswomen,
        format: val => `${val}`,
    },
    {
        name: 'user_smslevel',
        sortable: true,
        label: 'user_smslevel',
        align: 'left',
        field: row => row.user_smslevel,
        format: val => `${val}`,
    },
    {
        name: 'user_smsfinishdate',
        sortable: true,
        label: 'user_smsfinishdate',
        align: 'left',
        field: row => row.user_smsfinishdate,
        format: val => `${val}`,
    },
    {
        name: 'user_telegram_session',
        sortable: true,
        label: 'user_telegram_session',
        align: 'left',
        field: row => row.user_telegram_session,
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

      const readUrl = '/user/read'
      loading.value = true

      let query_params = _.defaults(Thinginfo.query_params.user ?? {},
      {
        filter,
        page,
        pageSize: rowsPerPage,
        order_by: JSON.stringify([[sortBy ? sortBy : 'id', descending ? 'desc' : 'asc']]),
        load_1_user_group: true,
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

