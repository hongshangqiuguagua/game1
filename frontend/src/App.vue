<template>
  <div class="app-container">
    <!-- 全局动画背景 -->
    <div class="global-animated-bg">
      <div class="animation-element element-1"></div>
      <div class="animation-element element-2"></div>
      <div class="animation-element element-3"></div>
      <div class="animation-element element-4"></div>
      <div class="animation-element element-5"></div>
      <div class="animation-element element-6"></div>
    </div>
    
    <!-- 后端服务不可用时的错误提示 -->
    <div v-if="showBackendError" class="backend-error">
      <div class="error-content">
        <h2>服务连接错误</h2>
        <p>{{ backendErrorMessage }}</p>
        <button @click="retryConnection" class="retry-button">重试连接</button>
      </div>
    </div>
    
    <router-view v-if="!showBackendError" v-slot="{ Component }">
      <transition name="page-transition" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
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
:root {
  --primary-color: #409eff;
  --primary-light: #66b1ff;
  --primary-dark: #3a8ee6;
  --success-color: #67c23a;
  --warning-color: #e6a23c;
  --danger-color: #f56c6c;
  --text-primary: #303133;
  --text-regular: #606266;
  --text-secondary: #909399;
  --bg-color: #f5f7fa;
  --border-color: #e4e7ed;
  --transition-duration: 0.3s;
  --box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

body {
  margin: 0;
  padding: 0;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: var(--bg-color);
  color: var(--text-regular);
  transition: background-color var(--transition-duration) ease;
}

.app-container {
  width: 100%;
  height: 100vh;
  position: relative;
  overflow: hidden;
}

/* 全局动画背景 */
.global-animated-bg {
  position: fixed;
  width: 100vw;
  height: 100vh;
  top: 0;
  left: 0;
  z-index: -1;
  pointer-events: none;
  overflow: hidden;
}

/* 动画元素 */
.animation-element {
  position: absolute;
  border-radius: 50%;
  opacity: 0.6;
  filter: blur(5px);
  pointer-events: none;
}

.element-1 {
  width: 100px;
  height: 100px;
  background-color: rgba(64, 158, 255, 0.3);
  top: 10%;
  right: 15%;
  animation: float1 25s infinite alternate;
}

.element-2 {
  width: 80px;
  height: 80px;
  background-color: rgba(103, 194, 58, 0.3);
  bottom: 15%;
  right: 20%;
  animation: float2 20s infinite alternate;
}

.element-3 {
  width: 120px;
  height: 120px;
  background-color: rgba(230, 162, 60, 0.3);
  top: 20%;
  left: 10%;
  animation: float3 30s infinite alternate;
}

.element-4 {
  width: 60px;
  height: 60px;
  background-color: rgba(245, 108, 108, 0.3);
  bottom: 25%;
  left: 25%;
  animation: float4 22s infinite alternate;
}

.element-5 {
  width: 150px;
  height: 150px;
  background-color: rgba(144, 147, 153, 0.2);
  top: 50%;
  left: 50%;
  animation: float5 35s infinite alternate;
}

.element-6 {
  width: 70px;
  height: 70px;
  background-color: rgba(103, 194, 58, 0.2);
  top: 70%;
  left: 10%;
  animation: float6 18s infinite alternate;
}

@keyframes float1 {
  0% { transform: translate(0, 0) rotate(0deg); }
  100% { transform: translate(-100px, 100px) rotate(360deg); }
}

@keyframes float2 {
  0% { transform: translate(0, 0) rotate(0deg); }
  100% { transform: translate(120px, -80px) rotate(-360deg); }
}

@keyframes float3 {
  0% { transform: translate(0, 0) rotate(0deg); }
  100% { transform: translate(150px, 70px) rotate(180deg); }
}

@keyframes float4 {
  0% { transform: translate(0, 0) rotate(0deg); }
  100% { transform: translate(-70px, -120px) rotate(-180deg); }
}

@keyframes float5 {
  0% { transform: translate(0, 0) rotate(0deg); }
  100% { transform: translate(-200px, -50px) rotate(270deg); }
}

@keyframes float6 {
  0% { transform: translate(0, 0) rotate(0deg); }
  100% { transform: translate(90px, 180px) rotate(360deg); }
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
  box-shadow: var(--box-shadow);
  animation: fadeInUp 0.5s ease-out;
}

.error-content h2 {
  color: var(--danger-color);
  margin-top: 0;
}

.retry-button {
  background-color: var(--primary-color);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  margin-top: 15px;
  transition: all var(--transition-duration) ease;
}

.retry-button:hover {
  background-color: var(--primary-light);
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 全局过渡效果 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity var(--transition-duration);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 页面过渡效果 */
.page-transition-enter-active,
.page-transition-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.page-transition-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.page-transition-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* 通用动画类 */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
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

/* 全局按钮增强 */
.el-button {
  transition: all var(--transition-duration) ease !important;
}

.el-button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
}

.el-button:active {
  transform: translateY(0) !important;
}

/* 卡片效果增强 */
.el-card {
  transition: all var(--transition-duration) ease !important;
  border-radius: 8px !important;
  overflow: hidden !important;
}

.el-card:hover {
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1) !important;
}

/* 更流畅的输入框效果 */
.el-input__inner {
  transition: all var(--transition-duration) ease !important;
}

.el-input__inner:focus {
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2) !important;
}
</style> 