// Zenit FrameWork 2024-11-24 15:52:50
import { boot } from 'quasar/wrappers'

import { QInput, QSlider, QSelect, QOptionGroup, QToggle, QDate, QCheckbox, 
  QTabs, QTab, QTabPanel, QTabPanels } from 'quasar'

import UserGrid from 'src/components/grids/UserGrid.vue'
import ProjectGrid from 'src/components/grids/ProjectGrid.vue'
import Project_UsersGrid from 'src/components/grids/Project_UsersGrid.vue'
import DttypeGrid from 'src/components/grids/DttypeGrid.vue'
import DtitemGrid from 'src/components/grids/DtitemGrid.vue'
import TopicGrid from 'src/components/grids/TopicGrid.vue'
import FederateGrid from 'src/components/grids/FederateGrid.vue'
import FederatetopicGrid from 'src/components/grids/FederatetopicGrid.vue'
import DiagramGrid from 'src/components/grids/DiagramGrid.vue'
import WikiGrid from 'src/components/grids/WikiGrid.vue'
import Wiki_TagsGrid from 'src/components/grids/Wiki_TagsGrid.vue'

export default boot(async ({ app }) => {
  app.component('QInput', QInput)
  app.component('QSlider', QSlider)
  app.component('QSelect', QSelect)
  app.component('QOptionGroup', QOptionGroup)
  app.component('QToggle', QToggle)
  app.component('QCheckbox', QCheckbox)
  app.component('QDate', QDate)

  app.component('UserGrid', UserGrid)
  app.component('ProjectGrid', ProjectGrid)
  app.component('Project_UsersGrid', Project_UsersGrid)
  app.component('DttypeGrid', DttypeGrid)
  app.component('DtitemGrid', DtitemGrid)
  app.component('TopicGrid', TopicGrid)
  app.component('FederateGrid', FederateGrid)
  app.component('FederatetopicGrid', FederatetopicGrid)
  app.component('DiagramGrid', DiagramGrid)
  app.component('WikiGrid', WikiGrid)
  app.component('Wiki_TagsGrid', Wiki_TagsGrid)

  app.component('QTabs', QTabs);
  app.component('QTab', QTab);
  app.component('QTabPanels', QTabPanels);
  app.component('QTabPanel', QTabPanel);
})


