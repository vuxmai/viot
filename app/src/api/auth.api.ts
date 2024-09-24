import type { LoginResponse, TokenResponse } from '@/types/auth.type'
import type { User } from '@/types/user.type'
import http from '@/lib/http'

export function login(data: {
  email: string
  password: string
}): Promise<LoginResponse> {
  return http.post('/auth/login', data)
}

export function register(data: {
  email: string
  password: string
  firstName: string
  lastName: string
}): Promise<User> {
  return http.post('/auth/register', data)
}

export function logout(): Promise<void> {
  return http.post('/auth/logout')
}

export function refresh(): Promise<TokenResponse> {
  return http.post('/auth/refresh')
}

export function forgotPassword(email: string): Promise<void> {
  return http.post('/auth/forgot-password', { email })
}

export function resetPassword(data: {
  email: string
  password: string
  token: string
}): Promise<void> {
  return http.post('/auth/reset-password', data)
}
