<template>
  <div class="login-container">
    <div class="login-card">
      <h2 class="title">登录</h2>
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="rules"
        label-position="top"
        @submit.prevent="handleLogin"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="loginForm.username" placeholder="请输入用户名" />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            show-password
          />
        </el-form-item>
        
        <div class="form-actions">
          <el-button
            type="primary"
            :loading="loading"
            @click="handleLogin"
            class="login-button pulse-button"
          >
            登录
          </el-button>
        </div>
      </el-form>
      
      <div class="form-footer">
        <p>
          还没有账号？
          <router-link to="/register" class="animated-link">立即注册</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'LoginView',
  
  setup() {
    const router = useRouter()
    const route = useRoute()
    const authStore = useAuthStore()
    const loginFormRef = ref(null)
    const loading = ref(false)
    
    // 登录表单数据
    const loginForm = reactive({
      username: '',
      password: ''
    })
    
    // 表单验证规则
    const rules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '用户名长度应为3-20个字符', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, max: 20, message: '密码长度应为6-20个字符', trigger: 'blur' }
      ]
    }
    
    // 登录处理函数
    const handleLogin = async () => {
      // 表单验证
      if (!loginFormRef.value) return
      
      await loginFormRef.value.validate(async (valid) => {
        if (valid) {
          loading.value = true
          
          try {
            // 调用登录接口
            const result = await authStore.login(loginForm.username, loginForm.password)
            
            if (result.success) {
              ElMessage.success('登录成功')
              
              // 如果有重定向地址，则跳转到重定向地址
              const redirectPath = route.query.redirect || '/game/levels'
              router.push(redirectPath)
            } else {
              ElMessage.error(result.message)
            }
          } catch (error) {
            console.error('登录失败:', error)
            ElMessage.error('登录失败，请稍后再试')
          } finally {
            loading.value = false
          }
        }
      })
    }
    
    return {
      loginFormRef,
      loginForm,
      rules,
      loading,
      handleLogin
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: transparent;
  position: relative;
  overflow: hidden;
  z-index: 1;
}

.login-card {
  width: 400px;
  padding: 30px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 2;
  animation: fadeInUp 0.8s ease-out;
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

.title {
  text-align: center;
  margin-bottom: 30px;
  color: #303133;
  position: relative;
}

.title::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 3px;
  background-color: #409eff;
  animation: expandWidth 1s ease-out forwards;
}

@keyframes expandWidth {
  from { width: 0; }
  to { width: 80px; }
}

.form-actions {
  margin-top: 20px;
}

.login-button {
  width: 100%;
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

.form-footer {
  margin-top: 20px;
  text-align: center;
  font-size: 14px;
  color: #606266;
}

.animated-link {
  color: #409eff;
  text-decoration: none;
  position: relative;
  transition: all 0.3s ease;
}

.animated-link::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background-color: #409eff;
  transition: width 0.3s ease;
}

.animated-link:hover::after {
  width: 100%;
}

.animated-link:hover {
  color: #66b1ff;
}
</style> 