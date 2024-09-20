export interface LoginResponse {
  accessToken: string
  refreshToken: string
  accessTokenExpiredAt: number
}

export type TokenResponse = LoginResponse
