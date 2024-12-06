<template>
  <q-layout view="hHh lpR fFf">

    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="mainMenu = !mainMenu" />

        <q-toolbar-title>
          ZENIT ADMIN UI
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

    <q-drawer show-if-above v-model="mainMenu" side="left" bordered>
      <essential-link  
          :title="$t('صفحه اول')" caption="" 
          link="#/" icon="local_library">
      </essential-link>
      <essential-link  
          title="کاربران" caption="user" 
          link="#/users" icon="data_object">
      </essential-link>
      <essential-link  
          title="پروژه" caption="project" 
          link="#/projects" icon="data_object">
      </essential-link>
      <essential-link  
          title="دسترسی پروژه" caption="project_users" 
          link="#/project_userss" icon="data_object">
      </essential-link>
      <essential-link  
          title="نوع داده" caption="dttype" 
          link="#/dttypes" icon="data_object">
      </essential-link>
      <essential-link  
          title="آیتم" caption="dtitem" 
          link="#/dtitems" icon="data_object">
      </essential-link>
      <essential-link  
          title="موضوع" caption="topic" 
          link="#/topics" icon="data_object">
      </essential-link>
      <essential-link  
          title="فدریت" caption="federate" 
          link="#/federates" icon="data_object">
      </essential-link>
      <essential-link  
          title="فدریت-تاپیک" caption="federatetopic" 
          link="#/federatetopics" icon="data_object">
      </essential-link>
      <essential-link  
          title="diagram" caption="diagram" 
          link="#/diagrams" icon="data_object">
      </essential-link>
      <essential-link  
          title="ویکی" caption="wiki" 
          link="#/wikis" icon="data_object">
      </essential-link>
      <essential-link  
          title="wiki_tags" caption="wiki_tags" 
          link="#/wiki_tagss" icon="data_object">
      </essential-link>
      <essential-link 
          title="پروفایل" caption="مشخصات شما" 
          link="#/user_profile" icon="remember_me">
      </essential-link>
      <essential-link 
          title="خروج" caption="خروج از حساب کاربری" 
          link="#/login" icon="logout">
      </essential-link>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-footer class="bg-grey-8 text-white">
      <q-bar>
        <div class="text-weight-bold">
          Zenit
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
import { api } from 'boot/axios'
import { useI18n } from 'vue-i18n'
import { useUserinfoStore } from 'stores/userinfo'
import ZenitUtils from 'src/ZenitUtils'
import EssentialLink from 'src/components/EssentialLink.vue'


export default {
  components: {
    EssentialLink
  },
  setup () {
    const userinfo = useUserinfoStore()

    const { t } = useI18n()

    const title = ref(t('الماس'))

    const { locale } = useI18n({ useScope: 'global' })
    const mainMenu = ref(false)
    
    return {
      locale,
      localeOptions: [
        { value: 'fa-IR', label: 'فارسی' },
        { value: 'en-US', label: 'English' },
      ],
      mainMenu, 
      userinfo,
      title
    }
  }
}
</script>

