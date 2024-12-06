<template>
  <q-layout view="hHh lpR fFf">

    <q-header elevated class="bg-primary text-white">
      <q-toolbar>

        <q-toolbar-title>
          {{ $t('الماس') }}
        </q-toolbar-title>
      
        <q-space></q-space>

        <q-btn-dropdown dense icon="language" label="">
          <q-list>

            <q-item v-for="l in localeOptions" :key="l.value"
              clickable v-close-popup @click="locale = l.value">
              <q-item-section>
                <q-item-label color="red">{{ l.label }}</q-item-label>
              </q-item-section>
              <q-item-section v-if="l.value == locale" side top>
                <q-icon name="check"/>
              </q-item-section>
            </q-item>

          </q-list>
        </q-btn-dropdown>
      
      </q-toolbar>
    </q-header>

    <q-page-container>
        <router-view />
    </q-page-container>

    <q-footer class="bg-grey-8 text-white">
      <q-bar>
        <div class="text-weight-bold">
          {{  $t('الماس - ابزار لایه ای مدیریت ارتباطات شبکه') }}
        </div>
        <q-space></q-space>
        <div>
          {{ zu.date2sh(new Date()) }}
        </div>
      </q-bar>
    </q-footer>

  </q-layout>

</template>

<script>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'


export default {
  components: {
  },
  setup () {
    const { locale } = useI18n({ useScope: 'global' })

    return {
      locale,
      localeOptions: [
        { value: 'fa-IR', label: 'فارسی' },
        { value: 'en-US', label: 'English' }
      ]
    }
  }
}
</script>