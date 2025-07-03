<template>
  <div class="start-container">
    <div class="content">
      <div class="header">
        <h1 class="title">火眼金睛 - 钓鱼邮件大挑战</h1>
        <p class="subtitle">提升您的网络安全意识，学会识别钓鱼邮件</p>
      </div>
      
      <div class="description">
        <p>在这个充满网络威胁的时代，钓鱼邮件是最常见的网络攻击方式之一。通过本游戏，您将学习如何识别各种类型的钓鱼邮件，保护自己免受网络诈骗的侵害。</p>
        <p>游戏规则简单：阅读邮件，判断是否为钓鱼邮件。如果您认为是钓鱼邮件，将其拖入垃圾桶；如果是正常邮件，则保留在收件箱中。</p>
      </div>
      
      <div class="actions">
        <el-button
          type="primary"
          size="large"
          @click="startGame"
          class="start-button pulse-button"
        >
          开始挑战
        </el-button>
      </div>
    </div>
    
    <div class="image-container">
      <div class="animation-wrapper">
        <img v-if="hasImage" src="@/assets/phishing-illustration.png" alt="钓鱼邮件示意图" class="main-image" />
        <div v-else class="fallback-animation">
          <div class="email-icon">
            <div class="email-body"></div>
            <div class="email-hook"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ref, onMounted } from 'vue'

export default {
  name: 'StartView',
  
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const hasImage = ref(true)
    
    // 检查图片是否存在
    onMounted(() => {
      const img = new Image()
      img.src = require('@/assets/phishing-illustration.png')
      img.onerror = () => {
        hasImage.value = false
      }
    })
    
    // 开始游戏按钮点击处理函数
    const startGame = () => {
      // 如果已登录，直接进入游戏
      if (authStore.isLoggedIn) {
        router.push('/game/levels')
      } else {
        // 否则跳转到登录页
        router.push('/login')
      }
    }
    
    return {
      startGame,
      hasImage
    }
  }
}
</script>

<style scoped>
.start-container {
  display: flex;
  min-height: 100vh;
  background: transparent;
  padding: 40px;
  position: relative;
  overflow: hidden;
  z-index: 1;
}

.content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding-right: 40px;
  position: relative;
  z-index: 2;
}

.header {
  margin-bottom: 30px;
  animation: fadeInUp 0.8s ease-out;
}

.title {
  font-size: 36px;
  color: #303133;
  margin-bottom: 10px;
  position: relative;
}

.title::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 80px;
  height: 3px;
  background-color: #409eff;
  animation: expandWidth 1s ease-out forwards;
}

@keyframes expandWidth {
  from { width: 0; }
  to { width: 80px; }
}

.subtitle {
  font-size: 18px;
  color: #606266;
  animation: fadeInUp 0.8s ease-out 0.2s both;
}

.description {
  margin-bottom: 40px;
  line-height: 1.6;
  color: #606266;
  animation: fadeInUp 0.8s ease-out 0.4s both;
}

.actions {
  margin-top: 20px;
  animation: fadeInUp 0.8s ease-out 0.6s both;
}

.start-button {
  padding: 15px 30px;
  font-size: 18px;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.pulse-button {
  animation: pulse 2s infinite;
  box-shadow: 0 0 0 rgba(64, 158, 255, 0.4);
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(64, 158, 255, 0.4);
    transform: scale(1);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(64, 158, 255, 0);
    transform: scale(1.02);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(64, 158, 255, 0);
    transform: scale(1);
  }
}

.start-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.4);
}

.start-button:active {
  transform: translateY(0);
}

.image-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.animation-wrapper {
  position: relative;
  z-index: 2;
  animation: floatAnimation 6s ease-in-out infinite;
}

.main-image {
  max-width: 100%;
  max-height: 500px;
  object-fit: contain;
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: all 0.5s ease;
}

.main-image:hover {
  transform: scale(1.03);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}

/* 无图片时的备用动画 */
.fallback-animation {
  width: 300px;
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: floatAnimation 6s ease-in-out infinite;
}

.email-icon {
  position: relative;
  width: 150px;
  height: 100px;
}

.email-body {
  position: absolute;
  width: 150px;
  height: 100px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}

.email-hook {
  position: absolute;
  width: 60px;
  height: 60px;
  border: 8px solid #e6413c;
  border-radius: 50%;
  border-bottom-color: transparent;
  transform: rotate(45deg);
  top: -30px;
  right: -20px;
  animation: rotateHook 8s linear infinite;
}

@keyframes rotateHook {
  0% { transform: rotate(45deg); }
  100% { transform: rotate(405deg); }
}

@keyframes floatAnimation {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式布局 */
@media (max-width: 768px) {
  .start-container {
    flex-direction: column;
    padding: 20px;
  }
  
  .content {
    padding-right: 0;
    margin-bottom: 30px;
  }
  
  .title {
    font-size: 28px;
  }
  
  .subtitle {
    font-size: 16px;
  }
}
</style> 