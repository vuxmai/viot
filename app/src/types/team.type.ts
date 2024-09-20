export interface TeamWithRole {
  id: string
  name: string
  slug: string
  description: string
  role: string
}

export interface Team {
  id: string
  name: string
  slug: string
  description: string
  default: boolean
  createdAt: Date
  updatedAt: Date
}
