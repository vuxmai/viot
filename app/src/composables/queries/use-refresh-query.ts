import { refresh } from '@/api/auth.api'
import { QUERY_KEYS } from '@/constants'
import { useQuery } from '@tanstack/vue-query'

export function useRefreshQuery() {
  return useQuery({
    queryKey: [QUERY_KEYS.refresh],
    queryFn: refresh,
    retry: false,
    refetchOnWindowFocus: false,
    meta: {
      ignoreGlobalToast: true
    }
  })
}
