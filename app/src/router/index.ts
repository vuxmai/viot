import { i18n } from '@/i18n'
import { useUserStore } from '@/stores'
import NProgress from 'nprogress'
import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import 'nprogress/nprogress.css'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/layouts/BaseLayout.vue'),
    redirect: '/dashboard',
    meta: {
      title: () => i18n.global.t('dashboard.title')
    },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/Dashboard.vue'),
        meta: {
          title: () => i18n.global.t('dashboard.title')
        }
      }

    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue'),
    meta: {
      title: () => i18n.global.t('login.title')
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/Register.vue'),
    meta: {
      title: () => i18n.global.t('register.title')
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

NProgress.configure({ showSpinner: false })

router.beforeEach((to, _, next) => {
  document.title = `${to?.meta.title?.() ?? ''} | Viot`
  NProgress.start()

  const userStore = useUserStore()

  if (to.meta.requireAuth && !userStore.isAuthenticated) {
    return toLogin(to.fullPath)
  }
  return next()
})

router.afterEach(() => {
  NProgress.done()
})

export function toLogin(path?: string): void {
  const userStore = useUserStore()
  userStore.logout()

  const currentPath = router.currentRoute.value.path
  currentPath !== '/login'
  && router.push({
    path: '/login',
    query: { to: path || (currentPath ?? undefined) }
  })
}

export default router
