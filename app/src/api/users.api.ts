import type { TeamWithRole } from '@/types/team.type'
import type { User } from '@/types/user.type'
import http from '@/lib/http'

export function getCurrentUser(): Promise<User> {
  return http.get('/users/me')
}

export function getCurrentTeams(): Promise<TeamWithRole[]> {
  return http.get('/users/me/teams')
}

export function updateCurrentUser(data: {
  firstName?: string
  lastName?: string
}): Promise<User> {
  return http.patch('/users/me', data)
}

export function updateCurrentUserPassword(data: {
  oldPassword: string
  newPassword: string
}): Promise<void> {
  return http.patch('/users/me/change-password', data)
}
