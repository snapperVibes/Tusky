import axios from 'axios'
import { apiUrl } from '@/env'
// import { IUserProfile, IUserProfileUpdate, IUserProfileCreate } from './interfaces'

// function authHeaders(token: String) {
//   return {
//     headers: {
//       Authorization: `Bearer ${token}`,
//     },
//   }
// }

export const api = {
  async logInGetToken (username: string, password: string) {
    const params = new URLSearchParams()
    params.append('username', username)
    params.append('password', password)

    return axios.post(`${apiUrl}/api/v1/login/access-token`, params)
  }
}
