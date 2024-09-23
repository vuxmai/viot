<script setup lang="ts">
import DashboardHeader from '@/components/DashboardHeader.vue'
import { useRefreshQuery } from '@/composables/queries/use-refresh-query'
import { useUserStore } from '@/stores/user.store'
import { LoaderCircle } from 'lucide-vue-next'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const router = useRouter()
const userStore = useUserStore()

const { data, isError, isPending } = userStore.accessToken
  ? { data: ref({ accessToken: userStore.accessToken }), isError: ref(false), isPending: ref(false) }
  : useRefreshQuery()

const accessToken = computed(() => data.value?.accessToken)

watchEffect(() => {
  if (accessToken.value) {
    userStore.setAccessToken(accessToken.value)
  }
})
watch(isError, (value) => {
  if (value) {
    userStore.logout()
    router.push('/login')
    toast.error({
      message: t('error.sessionExpired')
    })
  }
})
</script>

<template>
  <div class="w-full min-h-screen">
    <template v-if="isPending">
      <div class="flex items-center justify-center min-h-screen">
        <LoaderCircle class="w-16 h-16 animate-spin" />
      </div>
    </template>
    <template v-else>
      <DashboardHeader />
      <main class="flex flex-col items-center justify-center flex-1 gap-4 overflow-auto">
        <router-view />
      </main>
    </template>
  </div>
</template>
