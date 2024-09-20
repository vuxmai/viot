<script setup lang="ts">
import { useColorMode } from '@vueuse/core'
import { Notification, Notivue } from 'notivue'

useColorMode()
</script>

<template>
  <Notivue v-slot="item">
    <Notification :item="item" />
  </Notivue>

  <RouterView />
</template>
