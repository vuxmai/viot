import { getCurrentUser } from '@/api/users.api'
import { QUERY_KEYS } from '@/constants'
import { useQuery } from '@tanstack/vue-query'

export function useCurrentUserQuery() {
  return useQuery({
    queryKey: [QUERY_KEYS.currentUser],
    queryFn: getCurrentUser
  })
}
