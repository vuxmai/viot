import type { Team } from '@/types/team.type'
import http from '@/lib/http'

export function createTeam(data: {
  name: string
  description: string
}): Promise<Team> {
  return http.post('/teams', data)
}

export function updateTeam(
  id: string,
  data: {
    name?: string
    slug?: string
    description?: string
  }
): Promise<Team> {
  return http.patch(`/teams/${id}`, data)
}

export function deleteTeam(id: string): Promise<void> {
  return http.delete(`/teams/${id}`)
}
