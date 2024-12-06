// Zenit FrameWork 2024-12-06 14:15:58
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/first_page.vue') },
      { path: 'users', component: () => import('pages/user_page.vue') },
      { path: 'groups', component: () => import('pages/group_page.vue') },
      { path: 'assigns', component: () => import('pages/assign_page.vue') },
      { path: 'payments', component: () => import('pages/payment_page.vue') },
      { path: 'smss', component: () => import('pages/sms_page.vue') },
      
//      { path: 'project-edit/:q', component: () => import('pages/project_edit.vue') },
//      { path: 'dttype', component: () => import('pages/dttype_page.vue') },
//      { path: 'dttype-edit/:q', component: () => import('pages/dttype_edit.vue') },
//      { path: 'federates', component: () => import('pages/federate_page.vue') },
//      { path: 'payment', component: () => import('pages/user_payment.vue') },
//      { path: 'users', component: () => import('pages/user_list.vue') },
//      { path: 'groups', component: () => import('pages/user_groups.vue') },
    ]
  },
  {
    path: '/login',
    component: () => import('layouts/BlankLayout.vue'),
    children: [
      { path: '',component: () => import('pages/LoginPage.vue')}
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes


