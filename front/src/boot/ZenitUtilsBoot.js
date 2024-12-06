import { boot } from 'quasar/wrappers'
import ZenitUtils from 'src/ZenitUtils'
import _ from 'lodash'

export default boot(({ app }) => {
  app.config.globalProperties.zu = ZenitUtils
  app.config.globalProperties.z_ = _
})
