import type { User } from '@/types/user.type'
import { defineStore } from 'pinia'

const initialUserState: User = {
  id: '',
  firstName: '',
  lastName: '',
  email: '',
  role: '',
  createdAt: '',
  updatedAt: ''
}

export const useUserStore = defineStore('user', {
  state: () => ({
    user: { ...initialUserState },
    accessToken: '',
    expiresAt: new Date()
  }),
  getters: {
    isAuthenticated(): boolean {
      return !!this.accessToken && this.expiresAt > new Date()
    },
    fullName(): string {
      return `${this.user.firstName} ${this.user.lastName}`.trim()
    }
  },
  actions: {
    setUser(user: User) {
      this.user = user
    },
    setAccessToken(accessToken: string) {
      this.accessToken = accessToken
    },
    setExpiresAt(expiresAt: Date) {
      this.expiresAt = expiresAt
    },
    logout() {
      this.user = { ...initialUserState }
      this.accessToken = ''
      this.expiresAt = new Date()
    }
  }
})
