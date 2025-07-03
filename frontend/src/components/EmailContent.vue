<template>
  <div class="email-content-container">
    <transition name="fade" mode="out-in">
      <div v-if="email" class="email-content" :key="email.id">
        <div class="email-header">
          <!-- 邮件主题 -->
          <div class="email-subject">{{ email.subject }}</div>
          
          <!-- 发件人信息 -->
          <div class="email-sender-info">
            <div class="sender-avatar" :style="getAvatarColor()">{{ getSenderInitial() }}</div>
            <div class="sender-details">
              <div class="sender-name">{{ getSenderName() }}</div>
              <div class="sender-address">{{ email.sender }}</div>
              <div class="sender-date">{{ getRandomDate() }}</div>
            </div>
          </div>
          
          <!-- 收件人信息 -->
          <div class="email-recipients">
            <div class="recipient-item">
              <span class="label">收件人：</span>
              <span class="value">我</span>
            </div>
          </div>
        </div>
        
        <!-- 邮件工具栏 -->
        <div class="email-toolbar">
          <div class="toolbar-button" @click="animateButtonClick">
            <el-icon><el-icon-reply /></el-icon>
            <span>回复</span>
          </div>
          <div class="toolbar-button" @click="animateButtonClick">
            <el-icon><el-icon-share /></el-icon>
            <span>转发</span>
          </div>
          <div class="toolbar-button" @click="animateButtonClick">
            <el-icon><el-icon-delete /></el-icon>
            <span>删除</span>
          </div>
        </div>
        
        <!-- 邮件正文 -->
        <div class="email-body">
          <div v-html="formattedContent"></div>
        </div>
      </div>
      
      <div v-else class="empty-state" key="empty">
        <div class="empty-state-icon">
          <el-icon><el-icon-message /></el-icon>
        </div>
        <div class="empty-state-text">请选择一封邮件查看内容</div>
      </div>
    </transition>
  </div>
</template>

<script>
import { computed, ref } from 'vue'

export default {
  name: 'EmailContent',
  
  props: {
    email: {
      type: Object,
      default: null
    }
  },
  
  setup(props) {
    // 格式化邮件内容，将换行符转换为HTML标签
    const formattedContent = computed(() => {
      if (!props.email) return ''
      
      // 将普通链接转换为可点击的链接
      let content = props.email.content
        .replace(/\n/g, '<br>')
        .replace(/\[([^\]]+)\]\(([^)]+)\)/g, (match, text, url) => {
          // 处理Markdown格式的链接
          return `<a href="#" class="email-link" onclick="event.preventDefault()">${text}</a>`
        })
      
      return content
    })
    
    // 获取发件人姓名（从邮箱地址中提取）
    const getSenderName = () => {
      if (!props.email) return ''
      
      // 从邮件地址中提取名称部分
      const sender = props.email.sender
      if (sender.includes('@')) {
        const parts = sender.split('@')
        const name = parts[0]
        // 将下划线、点和连字符替换为空格，并首字母大写
        return name
          .replace(/[._-]/g, ' ')
          .replace(/\b\w/g, l => l.toUpperCase())
      }
      return sender
    }
    
    // 获取发件人首字母（用于头像）
    const getSenderInitial = () => {
      const name = getSenderName()
      return name ? name.charAt(0).toUpperCase() : '?'
    }
    
    // 生成随机日期（用于演示）
    const getRandomDate = () => {
      const today = new Date()
      const dates = [
        `${today.getFullYear()}年${today.getMonth() + 1}月${today.getDate()}日 ${Math.floor(Math.random() * 12) + 1}:${Math.floor(Math.random() * 60).toString().padStart(2, '0')}`,
        `${today.getFullYear()}年${today.getMonth() + 1}月${today.getDate() - 1}日 ${Math.floor(Math.random() * 12) + 1}:${Math.floor(Math.random() * 60).toString().padStart(2, '0')}`,
        `${today.getFullYear()}年${today.getMonth() + 1}月${today.getDate() - 2}日 ${Math.floor(Math.random() * 12) + 1}:${Math.floor(Math.random() * 60).toString().padStart(2, '0')}`
      ]
      return dates[Math.floor(Math.random() * dates.length)]
    }
    
    // 为发件人生成随机但一致的头像颜色
    const getAvatarColor = () => {
      if (!props.email) return { backgroundColor: '#0078d4' }
      
      // 基于发件人生成一致的颜色
      const colors = [
        '#0078d4', // 蓝色
        '#107c10', // 绿色
        '#d83b01', // 橙色
        '#b4009e', // 紫色
        '#5c2d91', // 深紫色
        '#008575', // 青色
        '#c19c00', // 金色
        '#e3008c'  // 粉色
      ]
      
      // 使用发件人字符串的哈希值来选择颜色
      const hashCode = props.email.sender.split('').reduce((hash, char) => {
        return ((hash << 5) - hash) + char.charCodeAt(0) | 0
      }, 0)
      
      const colorIndex = Math.abs(hashCode) % colors.length
      return { backgroundColor: colors[colorIndex] }
    }
    
    // 点击按钮动画
    const animateButtonClick = (event) => {
      const button = event.currentTarget
      button.classList.add('button-click-effect')
      setTimeout(() => {
        button.classList.remove('button-click-effect')
      }, 300)
    }
    
    return {
      formattedContent,
      getSenderName,
      getSenderInitial,
      getRandomDate,
      getAvatarColor,
      animateButtonClick
    }
  }
}
</script>

<style scoped>
.email-content-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: #fff;
  overflow: hidden;
}

/* 淡入淡出过渡效果 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

.email-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 邮件头部 */
.email-header {
  padding: 24px 32px;
  border-bottom: 1px solid #edebe9;
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.email-subject {
  font-size: 20px;
  font-weight: 600;
  color: #323130;
  margin-bottom: 16px;
  word-break: break-word;
}

.email-sender-info {
  display: flex;
  margin-bottom: 16px;
}

.sender-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #0078d4;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: bold;
  margin-right: 12px;
  flex-shrink: 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.sender-avatar:hover {
  transform: scale(1.1);
}

.sender-details {
  flex: 1;
}

.sender-name {
  font-weight: 600;
  color: #323130;
  margin-bottom: 4px;
}

.sender-address {
  font-size: 14px;
  color: #605e5c;
  margin-bottom: 4px;
}

.sender-date {
  font-size: 12px;
  color: #605e5c;
}

.email-recipients {
  margin-top: 16px;
  animation: fadeIn 0.5s ease-out 0.2s both;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.recipient-item {
  font-size: 14px;
  margin-bottom: 4px;
}

.label {
  color: #605e5c;
  margin-right: 4px;
}

.value {
  color: #323130;
  word-break: break-all;
}

/* 邮件工具栏 */
.email-toolbar {
  display: flex;
  gap: 16px;
  padding: 12px 32px;
  border-bottom: 1px solid #edebe9;
  animation: slideDown 0.3s ease-out 0.1s both;
}

.toolbar-button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 2px;
  cursor: pointer;
  color: #605e5c;
  font-size: 14px;
  transition: all 0.2s ease;
  background-color: transparent;
}

.toolbar-button:hover {
  background-color: #f3f2f1;
  color: #323130;
}

/* 按钮点击效果 */
@keyframes buttonClickWave {
  0% {
    transform: scale(0.95);
    background-color: #deecf9;
  }
  50% {
    transform: scale(1.02);
    background-color: #c7e0f4;
  }
  100% {
    transform: scale(1);
    background-color: #f3f2f1;
  }
}

.button-click-effect {
  animation: buttonClickWave 0.3s ease-out;
}

/* 邮件正文 */
.email-body {
  flex: 1;
  padding: 24px 32px;
  line-height: 1.6;
  color: #323130;
  overflow-y: auto;
  animation: fadeIn 0.5s ease-out 0.3s both;
}

/* 空状态 */
.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: #605e5c;
  animation: pulseIn 0.5s ease-out;
}

@keyframes pulseIn {
  0% {
    opacity: 0;
    transform: scale(0.9);
  }
  70% {
    opacity: 1;
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
}

.empty-state-icon {
  font-size: 48px;
  margin-bottom: 16px;
  color: #8a8886;
  animation: floatIcon 3s ease-in-out infinite;
}

@keyframes floatIcon {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.empty-state-text {
  font-size: 14px;
}

:deep(.email-link) {
  color: #0078d4;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

:deep(.email-link:hover) {
  text-decoration: underline;
  color: #106ebe;
}
</style> 