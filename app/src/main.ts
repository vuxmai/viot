import type { VueQueryPluginOptions } from '@tanstack/vue-query'
import { QueryCache, QueryClient, VueQueryPlugin } from '@tanstack/vue-query'
import { createNotivue } from 'notivue'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
import App from './App.vue'
import { i18n } from './i18n'
import router from './router'

import './assets/index.css'
import 'notivue/animations.css'
import 'notivue/notification.css'

const app = createApp(App)
const notivue = createNotivue()
const pinia = createPinia()

const queryClient = new QueryClient({
  queryCache: new QueryCache({
    onError: (error, query) => {
      if (query.meta?.ignoreGlobalToast) {
        return
      }

      if (query.meta?.errorMessage) {
        // @ts-expect-error - toast.error is not typed
        toast.error({ message: query.meta.errorMessage })
      }
      else {
        toast.error({ message: error.message })
      }
    }
  })
})
const queryPluginOptions: VueQueryPluginOptions = {
  queryClient
}

app.use(pinia)
app.use(VueQueryPlugin, queryPluginOptions)
app.use(router)
app.use(i18n)
app.use(notivue)

app.mount('#app')
