import axios from './axios'

// 用户注册
export const register = (username, password, email) => {
  return axios.post('/auth/register', { username, password, email })
}

// 用户登录
export const login = (username, password) => {
  return axios.post('/auth/login', { username, password })
}

// 游客登录
export const guestLogin = () => {
  return axios.post('/auth/guest-login')
}

// 刷新 token
export const refreshToken = () => {
  return axios.post('/auth/refresh')
}

// 获取用户资料
export const getUserProfile = () => {
  return axios.get('/auth/profile')
}

