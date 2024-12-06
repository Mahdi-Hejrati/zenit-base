// Zenit FrameWork 2024-12-06 14:15:58
import { boot } from 'quasar/wrappers'

import { QInput, QSlider, QSelect, QOptionGroup, QToggle, QDate, QCheckbox, 
  QTabs, QTab, QTabPanel, QTabPanels } from 'quasar'

import UserGrid from 'src/components/grids/UserGrid.vue'
import GroupGrid from 'src/components/grids/GroupGrid.vue'
import AssignGrid from 'src/components/grids/AssignGrid.vue'
import PaymentGrid from 'src/components/grids/PaymentGrid.vue'
import SmsGrid from 'src/components/grids/SmsGrid.vue'

export default boot(async ({ app }) => {
  app.component('QInput', QInput)
  app.component('QSlider', QSlider)
  app.component('QSelect', QSelect)
  app.component('QOptionGroup', QOptionGroup)
  app.component('QToggle', QToggle)
  app.component('QCheckbox', QCheckbox)
  app.component('QDate', QDate)

  app.component('UserGrid', UserGrid)
  app.component('GroupGrid', GroupGrid)
  app.component('AssignGrid', AssignGrid)
  app.component('PaymentGrid', PaymentGrid)
  app.component('SmsGrid', SmsGrid)

  app.component('QTabs', QTabs);
  app.component('QTab', QTab);
  app.component('QTabPanels', QTabPanels);
  app.component('QTabPanel', QTabPanel);
})


