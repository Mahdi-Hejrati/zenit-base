<template>
    <q-dialog ref="dialog" @hide="onDialogHide">
        <q-card class="q-dialog-plugin" style="direction: ltr">
            <q-card-section>
                <div class="text-h6 bg-red text-center text-white">Error</div>
            </q-card-section>
            <q-list>
                <q-item v-for="d in Data" :key="d">
                    <q-item-section>
                    <q-item-label caption>{{ d.loc?.join('.') }}</q-item-label>
                    <q-item-label lines="2">{{ d.msg }}</q-item-label>
                    <q-item-label caption lines="2">{{ d.ctx }}</q-item-label>
                    </q-item-section>

                    <q-item-section side top>
                    <q-item-label caption>{{ d.type }}</q-item-label>
                    </q-item-section>
                </q-item>

            </q-list>
            <q-card-actions align="right">
                <q-btn color="primary" label="OK" @click="onOKClick" />
            </q-card-actions>
        </q-card>
    </q-dialog>
</template>

<script>
import { ref } from 'vue'

export default {
    components: {
    },
    props: {
    },

    emits: [
        'ok', 'hide'
    ],

    methods: {
        show(row) {
            this.Data = row
            this.$refs.dialog.show()
        },

        hide() {
            this.$refs.dialog.hide()
        },

        onDialogHide() {
            this.$emit('hide')
        },

        onOKClick() {
            this.$emit('ok')
            this.hide()
        },

        onCancelClick() {
            this.hide()
        }
    },
    setup() {
        return {
            Data: ref({})
        }
    }
}
</script>
