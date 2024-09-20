import type { Page } from '@/types/pagination.type'
import type { TeamInvitation } from '@/types/team-invitation.type'
import http from '@/lib/http'

export function getTeamInvitations(
  teamId: string,
  paging: {
    page: number
    pageSize: number
  }
): Promise<Page<TeamInvitation>> {
  return http.get(`/teams/${teamId}/invitations`, { params: paging })
}

export function createTeamInvitation(
  teamId: string,
  data: {
    email: string
    role: string
  }
): Promise<TeamInvitation> {
  return http.post(`/teams/${teamId}/invitations`, data)
}

export function revokeTeamInvitation(
  teamId: string,
  invitationId: string
): Promise<void> {
  return http.delete(`/teams/${teamId}/invitations/${invitationId}`)
}

export function acceptTeamInvitation(token: string): Promise<void> {
  return http.post(`/teams/invitations/accept`, { token })
}

export function declineTeamInvitation(token: string): Promise<void> {
  return http.post(`/teams/invitations/decline`, { token })
}
