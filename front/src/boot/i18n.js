import { boot } from 'quasar/wrappers'
import { createI18n } from 'vue-i18n'
import messages from 'src/i18n'

export default boot(({ app }) => {
  const i18n = createI18n({
    locale: 'fa-IR',
    globalInjection: true,
    messages,
    silentTranslationWarn: true,
    missingWarn: false, 
    fallbackWarn: false,
  })

  // Set i18n instance on app
  app.use(i18n)
})
