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

        <div class="col-3 q-table__title">user</div>

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
      :columns="columns" optionName="userpage">
  </GridOptionsEditor>
  <ObjectDisplay ref="object_display">
  </ObjectDisplay>
  <UserEdit ref="edit_form" @hide="refresh_grid()" @ok="refresh_grid()">
  </UserEdit>
  <UserInsert ref="insert_form" @hide="refresh_grid()" @ok="refresh_grid()">
  </UserInsert>
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
import UserEdit from 'src/components/forms/UserEdit.vue'
import UserInsert from 'src/components/forms/UserInsert.vue'
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
  props: [],
  components: {
    GridOptionsEditor,
    ObjectDisplay,
    UserEdit,
    UserInsert,
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
      api.delete('/user/' + delete_row_id.value)
      .then(response=>{
        refresh_grid()
      })
    }

    return {
      label: t('user'),
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

