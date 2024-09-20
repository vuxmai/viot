<script setup lang="ts">
import { useRefreshQuery } from '@/composables/queries/use-refresh-query'
import { useUserStore } from '@/stores/user.store'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const router = useRouter()
const userStore = useUserStore()

const { data, isError } = useRefreshQuery()

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
    <main class="flex flex-col items-center justify-center flex-1 gap-4 overflow-auto">
      <router-view />
    </main>
  </div>
</template>
