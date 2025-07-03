import { defineStore } from 'pinia'
import http from '@/utils/http'
import { useAuthStore } from './auth'

export const useGameStore = defineStore('game', {
  state: () => ({
    levels: [],
    currentLevel: null,
    emails: [],
    readEmails: new Set(),
    trashEmails: new Set(),
    selectedEmail: null,
    gameResult: null,
    summary: null,
    loading: false,
    error: null
  }),
  
  getters: {
    // 获取当前关卡信息
    getCurrentLevel: (state) => state.currentLevel,
    
    // 获取所有邮件
    getEmails: (state) => state.emails,
    
    // 获取收件箱中的邮件（不在垃圾桶中的邮件）
    getInboxEmails: (state) => state.emails.filter(email => !state.trashEmails.has(email.id)),
    
    // 获取垃圾桶中的邮件
    getTrashEmails: (state) => state.emails.filter(email => state.trashEmails.has(email.id)),
    
    // 判断邮件是否已读
    isEmailRead: (state) => (emailId) => state.readEmails.has(emailId),
    
    // 判断邮件是否在垃圾桶中
    isEmailInTrash: (state) => (emailId) => state.trashEmails.has(emailId),
    
    // 获取当前选中的邮件
    getSelectedEmail: (state) => state.selectedEmail,
    
    // 获取游戏结果
    getGameResult: (state) => state.gameResult,
    
    // 获取游戏总结
    getGameSummary: (state) => state.summary
  },
  
  actions: {
    // 获取所有关卡
    async fetchLevels() {
      try {
        this.loading = true
        this.error = null
        
        const response = await http.get('/api/game/levels')
        this.levels = response.data
        
        return { success: true, levels: this.levels }
      } catch (error) {
        console.error('获取关卡失败:', error)
        this.error = error.response?.data?.detail || '获取关卡失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },
    
    // 获取关卡邮件
    async fetchLevelEmails(levelId) {
      try {
        this.loading = true
        this.error = null
        
        // 重置状态
        this.readEmails = new Set()
        this.trashEmails = new Set()
        this.selectedEmail = null
        this.gameResult = null
        
        // 获取关卡信息
        const levelIndex = this.levels.findIndex(level => level.id === parseInt(levelId))
        if (levelIndex !== -1) {
          this.currentLevel = this.levels[levelIndex]
        } else {
          // 如果levels还未加载，先加载levels
          await this.fetchLevels()
          this.currentLevel = this.levels.find(level => level.id === parseInt(levelId))
        }
        
        if (!this.currentLevel) {
          throw new Error('关卡不存在')
        }
        
        // 获取邮件列表
        const response = await http.get(`/api/game/levels/${levelId}/emails`)
        this.emails = response.data
        
        return { success: true, emails: this.emails }
      } catch (error) {
        console.error('获取关卡邮件失败:', error)
        this.error = error.response?.data?.detail || '获取关卡邮件失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },
    
    // 选择邮件
    selectEmail(emailId) {
      const email = this.emails.find(email => email.id === emailId)
      if (email) {
        this.selectedEmail = email
        this.readEmails.add(emailId)
      }
    },
    
    // 将邮件移入垃圾桶
    moveToTrash(emailId) {
      console.log(`将邮件 ${emailId} 移入垃圾桶`);
      if (!emailId) {
        console.error('移动邮件到垃圾桶错误: 无效的邮件ID');
        return false;
      }
      
      // 检查邮件是否存在
      const email = this.emails.find(email => email.id === emailId);
      if (!email) {
        console.error(`移动邮件到垃圾桶错误: 邮件ID ${emailId} 不存在`);
        return false;
      }
      
      this.trashEmails.add(emailId);
      
      // 如果当前选中的邮件被移入垃圾桶，取消选中
      if (this.selectedEmail && this.selectedEmail.id === emailId) {
        this.selectedEmail = null;
      }
      
      console.log(`邮件 ${emailId} 已成功移入垃圾桶`);
      return true;
    },
    
    // 从垃圾桶恢复邮件
    restoreFromTrash(emailId) {
      console.log(`从垃圾桶恢复邮件 ${emailId}`);
      if (!emailId) {
        console.error('从垃圾桶恢复邮件错误: 无效的邮件ID');
        return false;
      }
      
      // 检查邮件是否存在
      const email = this.emails.find(email => email.id === emailId);
      if (!email) {
        console.error(`从垃圾桶恢复邮件错误: 邮件ID ${emailId} 不存在`);
        return false;
      }
      
      // 检查邮件是否在垃圾桶中
      if (!this.trashEmails.has(emailId)) {
        console.warn(`邮件 ${emailId} 不在垃圾桶中，无需恢复`);
        return false;
      }
      
      this.trashEmails.delete(emailId);
      console.log(`邮件 ${emailId} 已成功从垃圾桶恢复`);
      return true;
    },
    
    // 提交关卡结果
    async submitLevel(levelId, judgments = null) {
      try {
        this.loading = true
        this.error = null
        
        // 如果没有传入判断结果，则使用当前状态生成
        if (!judgments) {
          judgments = this.emails.map(email => ({
            email_id: email.id,
            is_phishing_guess: this.trashEmails.has(email.id)
          }))
        }
        
        console.log('提交判断结果:', judgments)
        
        // 提交结果
        const response = await http.post(
          `/api/game/levels/${levelId}/submit`,
          { judgments }
        )
        
        this.gameResult = {
          ...response.data,
          level_name: response.data.level_name || '',
          trick_summary: response.data.trick_summary || '',
        }
        
        console.log('提交关卡结果成功:', this.gameResult)
        
        return { success: true, result: this.gameResult }
      } catch (error) {
        console.error('提交关卡结果失败:', error)
        this.error = error.response?.data?.detail || '提交关卡结果失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },
    
    // 获取游戏总结
    async fetchGameSummary() {
      try {
        this.loading = true
        this.error = null
        
        const response = await http.get('/api/game/summary')
        this.summary = response.data
        
        return { success: true, summary: this.summary }
      } catch (error) {
        console.error('获取游戏总结失败:', error)
        this.error = error.response?.data?.detail || '获取游戏总结失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },
    
    // 重置游戏状态
    resetGameState() {
      this.currentLevel = null
      this.emails = []
      this.readEmails = new Set()
      this.trashEmails = new Set()
      this.selectedEmail = null
      this.gameResult = null
      this.error = null
    }
  }
}) 