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
          class="start-button"
        >
          开始挑战
        </el-button>
      </div>
    </div>
    
    <div class="image-container">
      <img src="@/assets/phishing-illustration.png" alt="钓鱼邮件示意图" class="main-image" />
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'StartView',
  
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
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
      startGame
    }
  }
}
</script>

<style scoped>
.start-container {
  display: flex;
  min-height: 100vh;
  background-color: #f5f7fa;
  padding: 40px;
}

.content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding-right: 40px;
}

.header {
  margin-bottom: 30px;
}

.title {
  font-size: 36px;
  color: #303133;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 18px;
  color: #606266;
}

.description {
  margin-bottom: 40px;
  line-height: 1.6;
  color: #606266;
}

.actions {
  margin-top: 20px;
}

.start-button {
  padding: 15px 30px;
  font-size: 18px;
}

.image-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.main-image {
  max-width: 100%;
  max-height: 500px;
  object-fit: contain;
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