import type { AxiosError } from 'axios'

interface ErrorResponse {
  status: number
  errorCode: string
  message: string
}

declare module '@tanstack/vue-query' {
  interface Register {
    defaultError: AxiosError<ErrorResponse>
  }
}
