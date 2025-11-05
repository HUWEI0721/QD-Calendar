import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login, register, guestLogin, getUserProfile } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(null)
  
  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isGuest = computed(() => user.value?.role === 'guest')
  
  // 登录
  async function loginUser(username, password) {
    try {
      const response = await login(username, password)
      token.value = response.access_token
      user.value = response.user
      localStorage.setItem('token', response.access_token)
      return { success: true, user: response.user }
    } catch (error) {
      return { success: false, message: error.response?.data?.message || '登录失败' }
    }
  }
  
  // 注册
  async function registerUser(username, password, email) {
    try {
      const response = await register(username, password, email)
      return { success: true, user: response.user }
    } catch (error) {
      return { success: false, message: error.response?.data?.message || '注册失败' }
    }
  }
  
  // 游客登录
  async function loginAsGuest() {
    try {
      const response = await guestLogin()
      token.value = response.access_token
      user.value = response.user
      localStorage.setItem('token', response.access_token)
      return { success: true, user: response.user }
    } catch (error) {
      return { success: false, message: error.response?.data?.message || '游客登录失败' }
    }
  }
  
  // 登出
  function logout() {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
  }
  
  // 检查认证状态
  async function checkAuth() {
    if (!token.value) {
      return false
    }
    
    try {
      const response = await getUserProfile()
      user.value = response
      return true
    } catch (error) {
      // token 无效，清除登录状态
      logout()
      return false
    }
  }
  
  return {
    token,
    user,
    isAuthenticated,
    isAdmin,
    isGuest,
    loginUser,
    registerUser,
    loginAsGuest,
    logout,
    checkAuth
  }
})

