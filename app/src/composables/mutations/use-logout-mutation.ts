import { logout } from '@/api/auth.api'
import { useMutation } from '@tanstack/vue-query'

export function useLogoutMutation() {
  return useMutation({
    mutationFn: logout
  })
}
