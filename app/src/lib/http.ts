import type { ErrorResponse } from '@/types/error-registration'
import type { AxiosError } from 'axios'
import { refresh } from '@/api/auth.api'
import { toLogin } from '@/router'
import { useUserStore } from '@/stores/user.store'
import axios from 'axios'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

const instance = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000,
  withCredentials: true
})

const userStore = useUserStore()

let isRefreshing = false
let refreshSubscribers: ((token: string) => void)[] = []

function subscribeTokenRefresh(cb: (token: string) => void) {
  refreshSubscribers.push(cb)
}

function onRefreshed(token: string) {
  refreshSubscribers.forEach(cb => cb(token))
  refreshSubscribers = []
}

function isTokenExpired(error: AxiosError<ErrorResponse>) {
  return error.response?.status === 401 && ['TOKEN_EXPIRED', 'INVALID_TOKEN'].includes(error.response?.data.errorCode)
}

instance.interceptors.request.use(
  (config) => {
    NProgress.start()
    const token = userStore.accessToken
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (err) => {
    return Promise.reject(err)
  }
)

instance.interceptors.response.use(
  (response) => {
    NProgress.done()
    return Promise.resolve(response.data)
  },
  async (error: AxiosError<ErrorResponse>) => {
    NProgress.done()
    if (isTokenExpired(error)) {
      const originalRequest = error.config

      if (!isRefreshing) {
        isRefreshing = true

        try {
          const response = await refresh()
          const newToken = response.accessToken
          userStore.setAccessToken(newToken)
          onRefreshed(newToken)
          isRefreshing = false

          if (originalRequest) {
            originalRequest.headers.Authorization = `Bearer ${newToken}`
            return instance(originalRequest)
          }
        }
        catch {
          isRefreshing = false
          toast.error({
            message: 'Session expired. Please login again.'
          })
          toLogin()
          return
        }
      }

      return new Promise((resolve) => {
        subscribeTokenRefresh((token: string) => {
          if (originalRequest) {
            originalRequest.headers.Authorization = `Bearer ${token}`
            resolve(instance(originalRequest))
          }
        })
      })
    }

    if (error.response?.status === 401 && window.location.pathname !== '/login') {
      toast.error({
        message: 'Session expired. Please login again.'
      })
      toLogin()
      return Promise.reject(error)
    }

    if (error.response?.status === 403) {
      toast.error({
        message: 'You do not have permission to access this resource.'
      })
      return Promise.reject(error)
    }

    return Promise.reject(error)
  }
)

export default instance
