import { defineStore } from 'pinia'
import http from '@/utils/http'
import { useAuthStore } from './auth'

export const useAdminStore = defineStore('admin', {
  state: () => ({
    levels: [],
    emails: [],
    statistics: [],
    overallStats: null,
    loading: false,
    error: null,
    emailStats: []
  }),
  
  actions: {
    // 获取所有关卡（管理员视图）
    async fetchLevels() {
      try {
        this.loading = true
        this.error = null
        
        const response = await http.get('/api/admin/levels')
        this.levels = response.data
        
        return { success: true, levels: this.levels, data: response.data }
      } catch (error) {
        console.error('获取关卡失败:', error)
        this.error = error.response?.data?.detail || '获取关卡失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },
    
    // 创建新关卡
    async createLevel(levelData) {
      try {
        this.loading = true
        this.error = null
        
        const response = await http.post('/api/admin/levels', levelData)
        this.levels.push(response.data)
        
        return { success: true, data: response.data }
      } catch (error) {
        console.error('创建关卡失败:', error)
        this.error = error.response?.data?.detail || '创建关卡失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },
    
    // 更新关卡
    async updateLevel(levelData) {
      try {
        this.loading = true
        this.error = null
        
        const response = await http.put(`/api/admin/levels/${levelData.id}`, levelData)
        const index = this.levels.findIndex(l => l.id === levelData.id)
        if (index !== -1) {
          this.levels[index] = response.data
        }
        
        return { success: true, data: response.data }
      } catch (error) {
        console.error('更新关卡失败:', error)
        this.error = error.response?.data?.detail || '更新关卡失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },
    
    // 删除关卡
    async deleteLevel(levelId) {
      try {
        this.loading = true
        this.error = null
        
        await http.delete(`/api/admin/levels/${levelId}`)
        this.levels = this.levels.filter(l => l.id !== levelId)
        
        return { success: true }
      } catch (error) {
        console.error('删除关卡失败:', error)
        this.error = error.response?.data?.detail || '删除关卡失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },
    
    // 获取关卡下的所有邮件
    async fetchLevelEmails(levelId) {
      try {
        this.loading = true
        this.error = null
        
        const response = await http.get(`/api/admin/levels/${levelId}/emails`)
        this.emails = response.data || []
        
        return this.emails
      } catch (error) {
        console.error('获取邮件失败:', error)
        this.error = error.response?.data?.detail || '获取邮件失败'
        this.emails = []
        return []
      } finally {
        this.loading = false
      }
    },
    
    // 创建新邮件
    async createEmail(emailData) {
      try {
        this.loading = true
        this.error = null
        
        const response = await http.post('/api/admin/emails', emailData)
        
        // 更新本地邮件列表
        await this.fetchLevelEmails(emailData.level_id)
        
        return { success: true, email: response.data }
      } catch (error) {
        console.error('创建邮件失败:', error)
        this.error = error.response?.data?.detail || '创建邮件失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },
    
    // 更新邮件
    async updateEmail(emailId, emailData) {
      try {
        this.loading = true
        this.error = null
        
        const response = await http.put(`/api/admin/emails/${emailId}`, emailData)
        
        // 更新本地邮件列表
        const levelId = this.emails.find(email => email.id === emailId)?.level_id
        if (levelId) {
          await this.fetchLevelEmails(levelId)
        }
        
        return { success: true, email: response.data }
      } catch (error) {
        console.error('更新邮件失败:', error)
        this.error = error.response?.data?.detail || '更新邮件失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },
    
    // 删除邮件
    async deleteEmail(emailId) {
      try {
        this.loading = true
        this.error = null
        
        // 保存当前邮件所属关卡ID
        const levelId = this.emails.find(email => email.id === emailId)?.level_id
        
        await http.delete(`/api/admin/emails/${emailId}`)
        
        // 更新本地邮件列表
        if (levelId) {
          await this.fetchLevelEmails(levelId)
        }
        
        return { success: true }
      } catch (error) {
        console.error('删除邮件失败:', error)
        this.error = error.response?.data?.detail || '删除邮件失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },
    
    // 获取邮件错误率统计
    async fetchEmailStatistics() {
      try {
        this.loading = true
        this.error = null
        
        const response = await http.get('/api/admin/statistics/emails')
        this.statistics = response.data || []
        
        return { success: true, statistics: this.statistics }
      } catch (error) {
        console.error('获取统计信息失败:', error)
        this.error = error.response?.data?.detail || '获取统计信息失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },
    
    // 获取总体统计数据
    async fetchOverallStatistics() {
      try {
        this.loading = true
        this.error = null
        
        const response = await http.get('/api/admin/statistics/overview')
        this.overallStats = response.data
        
        return { success: true, statistics: this.overallStats }
      } catch (error) {
        console.error('获取总体统计信息失败:', error)
        this.error = error.response?.data?.detail || '获取总体统计信息失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },
    
    async fetchEmailStats() {
      this.loading = true;
      this.error = null;
      try {
        const response = await http.get('/api/admin/statistics/emails');
        this.emailStats = response.data || [];
        return { success: true };
      } catch (error) {
        console.error('获取邮件统计失败:', error);
        this.error = error.response?.data?.detail || '获取邮件统计失败';
        return { success: false, message: this.error };
      } finally {
        this.loading = false;
      }
    }
  }
}) 