import { defineStore } from 'pinia'
import http from '@/utils/http'
import { API_BASE_URL } from '@/utils/config'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null,
    backendStatus: null
  }),
  
  getters: {
    isLoggedIn: (state) => !!state.token,
    isAdmin: (state) => {
      const isAdmin = state.user?.is_admin || false;
      console.log(`当前用户管理员状态: ${isAdmin}, 用户:`, state.user);
      return isAdmin;
    },
    getUser: (state) => state.user,
    isBackendAvailable: (state) => state.backendStatus === 'ok'
  },
  
  actions: {
    // 检查后端服务是否可用
    async checkBackendHealth() {
      try {
        console.log('正在检查后端服务健康状态...');
        const response = await http.get('/health');
        this.backendStatus = response.data.status;
        console.log(`后端服务健康状态: ${this.backendStatus}`);
        return { success: true, status: this.backendStatus };
      } catch (error) {
        console.error('后端服务不可用:', error);
        this.backendStatus = 'error';
        return { 
          success: false, 
          message: '无法连接到后端服务，请稍后再试'
        };
      }
    },
  
    async login(username, password) {
      try {
        // 先检查后端健康状态
        const healthCheck = await this.checkBackendHealth();
        if (!healthCheck.success) {
          return healthCheck; // 如果后端不可用，直接返回错误
        }
        
        // 创建表单数据（OAuth2要求的格式）
        const formData = new FormData()
        formData.append('username', username)
        formData.append('password', password)
        
        console.log(`尝试登录: 用户名=${username}`);
        
        // 发送登录请求
        const response = await http.post('/api/auth/login', formData)
        
        // 保存令牌
        this.token = response.data.access_token
        localStorage.setItem('token', this.token)
        console.log(`登录成功，获取到token: ${this.token.substring(0, 15)}...`);
        
        // 获取用户信息
        await this.fetchUserInfo()
        
        return { success: true }
      } catch (error) {
        console.error('登录失败:', error)
        return { 
          success: false, 
          message: error.response?.data?.detail || '登录失败，请检查用户名和密码'
        }
      }
    },
    
    async register(username, email, password) {
      try {
        // 发送注册请求
        await http.post('/api/auth/register', {
          username,
          email,
          password
        })
        
        // 注册成功后自动登录
        return await this.login(username, password)
      } catch (error) {
        console.error('注册失败:', error)
        return { 
          success: false, 
          message: error.response?.data?.detail || '注册失败，请稍后再试'
        }
      }
    },
    
    async fetchUserInfo() {
      try {
        // 获取用户信息
        const response = await http.get('/api/auth/me')
        
        // 保存用户信息
        this.user = response.data
        console.log('获取用户信息成功:', this.user);
        localStorage.setItem('user', JSON.stringify(this.user))
        
        return { success: true }
      } catch (error) {
        console.error('获取用户信息失败:', error)
        this.logout()
        return { 
          success: false, 
          message: '获取用户信息失败，请重新登录'
        }
      }
    },
    
    logout() {
      // 清除令牌和用户信息
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      console.log('用户已登出');
    }
  }
}) 