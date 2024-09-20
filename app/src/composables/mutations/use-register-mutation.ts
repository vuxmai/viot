import { register } from '@/api/auth.api'
import { useMutation } from '@tanstack/vue-query'

export function useRegisterMutation() {
  return useMutation({
    mutationFn: register
  })
}
