// Zenit FrameWork 2024-11-24 15:52:51
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/first_page.vue') },
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


