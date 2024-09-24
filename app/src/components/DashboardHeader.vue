<script setup lang="ts">
import { useLogoutMutation } from '@/composables/mutations/use-logout-mutation'
import { useCurrentUserQuery } from '@/composables/queries/use-current-user-query'
import { CircleUser, LogOut } from 'lucide-vue-next'
import { RouterLink } from 'vue-router'

const { data: currentUser } = useCurrentUserQuery()
const { mutate: logoutMutate } = useLogoutMutation()
</script>

<template>
  <header
    class="border-b border-b-gray-200 flex h-8 items-center justify-between gap-4 px-4 lg:h-[60px] lg:px-4 bg-red-400"
  >
    <RouterLink to="/">
      <div class="flex items-center justify-center w-8 h-8 bg-gray-100 rounded-full">
        <img src="@/assets/logo.svg" alt="logo" class="h-4">
      </div>
    </RouterLink>
    <TeamSwitcher />

    <div class="relative flex-1 ml-auto grow-0">
      <!-- <PopoverNotification /> -->
    </div>
    <DropdownMenu>
      <DropdownMenuTrigger as-child>
        <Button variant="secondary" size="icon" class="w-8 h-8 rounded-full">
          <CircleUser class="w-5 h-5" />
          <span class="sr-only">Toggle user menu</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuLabel>{{ currentUser!.firstName }}</DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuItem @click="() => $router.push({ name: 'OrganizationSettings' })">
          Dashboard
        </DropdownMenuItem>
        <DropdownMenuItem>
          <RouterLink to="/account" class="w-full">
            Account Settings
          </RouterLink>
        </DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem class="text-red-500 duration-300 hover:bg-red-100 bg-red-50">
          <div class="flex items-center gap-1" @click="logoutMutate()">
            <LogOut class="w-3.5 h-3.5 text-red-500" />
            Logout
          </div>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  </header>
</template>
