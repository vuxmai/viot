import 'vue-router'

// https://router.vuejs.org/guide/advanced/meta.html
export {}

declare module 'vue-router' {
  interface RouteMeta {
    title: (() => string)
    requireAuth?: boolean
  }
}
