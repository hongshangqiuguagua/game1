import axios from 'axios'
import router from '@/router'
import { API_BASE_URL } from '@/utils/config'

// 创建axios实例
const http = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000
})

// 请求拦截器
http.interceptors.request.use(
  config => {
    // 从localStorage获取token
    const token = localStorage.getItem('token')
    
    // 如果有token，添加到请求头
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    
    console.log(`发送请求: ${config.method.toUpperCase()} ${config.url}`)
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
http.interceptors.response.use(
  response => {
    console.log(`接收响应: ${response.config.method.toUpperCase()} ${response.config.url} - 状态码: ${response.status}`)
    return response
  },
  error => {
    const { response } = error
    
    if (response) {
      console.error(`请求失败: ${response.config.method.toUpperCase()} ${response.config.url} - 状态码: ${response.status}`)
      console.error('错误详情:', response.data)
      
      // 处理不同的HTTP错误
      switch (response.status) {
        case 401:
          // 未认证错误处理
          console.log('用户未认证，清除认证信息并重定向到登录页')
          // 清除本地token
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          
          // 如果不是登录页面，重定向到登录页
          if (router.currentRoute.value.name !== 'Login') {
            router.push({
              name: 'Login',
              query: { redirect: router.currentRoute.value.fullPath }
            })
          }
          break
          
        case 403:
          console.log('权限不足，无法访问此资源')
          // 可以选择重定向到错误页面或首页
          break
          
        case 404:
          console.log('请求的资源不存在')
          break
          
        case 500:
          console.log('服务器内部错误')
          break
      }
    } else {
      console.error('请求失败，无法连接到服务器', error.message)
    }
    
    return Promise.reject(error)
  }
)

export default http 