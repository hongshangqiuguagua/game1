<template>
  <div class="app-container">
    <!-- 后端服务不可用时的错误提示 -->
    <div v-if="showBackendError" class="backend-error">
      <div class="error-content">
        <h2>服务连接错误</h2>
        <p>{{ backendErrorMessage }}</p>
        <button @click="retryConnection" class="retry-button">重试连接</button>
      </div>
    </div>
    
    <router-view v-if="!showBackendError" />
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth';
import { onMounted, ref } from 'vue';

export default {
  name: 'App',
  setup() {
    const authStore = useAuthStore();
    const showBackendError = ref(false);
    const backendErrorMessage = ref('无法连接到后端服务，请检查网络连接或联系管理员。');
    const connectionCheckInterval = ref(null);
    
    // 检查后端服务连接
    const checkBackendConnection = async () => {
      const result = await authStore.checkBackendHealth();
      if (!result.success) {
        showBackendError.value = true;
        backendErrorMessage.value = result.message || '无法连接到后端服务，请检查网络连接或联系管理员。';
      } else {
        showBackendError.value = false;
      }
    };
    
    // 重试连接
    const retryConnection = async () => {
      await checkBackendConnection();
    };
    
    onMounted(async () => {
      // 首次检查
      await checkBackendConnection();
      
      // 设置定时检查（每30秒检查一次）
      connectionCheckInterval.value = setInterval(async () => {
        if (!showBackendError.value) {
          await checkBackendConnection();
        }
      }, 30000);
    });
    
    return {
      showBackendError,
      backendErrorMessage,
      retryConnection
    };
  }
};
</script>

<style>
body {
  margin: 0;
  padding: 0;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f5f7fa;
}

.app-container {
  width: 100%;
  height: 100vh;
  position: relative;
}

/* 后端错误提示样式 */
.backend-error {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.error-content {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  text-align: center;
  max-width: 400px;
}

.error-content h2 {
  color: #f56c6c;
  margin-top: 0;
}

.retry-button {
  background-color: #409eff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  margin-top: 15px;
}

.retry-button:hover {
  background-color: #66b1ff;
}

/* 全局过渡效果 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style> 