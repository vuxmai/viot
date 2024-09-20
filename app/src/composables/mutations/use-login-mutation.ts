import { login } from '@/api/auth.api'
import { useMutation } from '@tanstack/vue-query'

export function useLoginMutation() {
  return useMutation({
    mutationFn: login
  })
}
