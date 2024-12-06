<template>
    <q-dialog ref="dialog" @hide="onDialogHide">
        <q-card class="q-dialog-plugin" style="direction: ltr">
            <q-card-section>
                <div class="text-h6 text-center bg-primary text-white">Object JSON</div>
            </q-card-section>
            <div class="q-ma-sm">
                <pre>
{{ JSON.stringify(Data, 2, 2) }}
                </pre>
            </div>
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
