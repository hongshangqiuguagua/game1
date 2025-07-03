<template>
  <div class="game-layout">
    <el-container>
      <el-header height="60px">
        <div class="header-content">
          <div class="logo">
            <h2>钓鱼邮件识别游戏</h2>
          </div>
          <div class="user-info">
            <span v-if="user">{{ user.username }}</span>
            <el-dropdown @command="handleCommand">
              <el-button icon="el-icon-setting" circle></el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="summary">查看总结</el-dropdown-item>
                  <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                  <el-dropdown-item v-if="isAdmin" command="admin">管理后台</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </el-header>
      
      <el-main>
        <router-view />
      </el-main>
      
      <el-footer height="40px">
        <div class="footer-content">
          <p>© 2023 钓鱼邮件识别教学游戏 | 提升网络安全意识</p>
        </div>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'GameLayout',
  
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    // 获取当前用户
    const user = computed(() => authStore.getUser)
    
    // 判断是否为管理员
    const isAdmin = computed(() => authStore.isAdmin)
    
    // 下拉菜单命令处理
    const handleCommand = (command) => {
      switch (command) {
        case 'summary':
          router.push('/summary')
          break
        case 'admin':
          router.push('/admin')
          break
        case 'logout':
          ElMessageBox.confirm('确定要退出登录吗？', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            authStore.logout()
            router.push('/')
          }).catch(() => {})
          break
      }
    }
    
    return {
      user,
      isAdmin,
      handleCommand
    }
  }
}
</script>

<style scoped>
.game-layout {
  height: 100vh;
}

.el-container {
  height: 100%;
}

.el-header {
  background-color: #409eff;
  color: #fff;
  line-height: 60px;
  padding: 0 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo h2 {
  margin: 0;
  font-size: 20px;
}

.user-info {
  display: flex;
  align-items: center;
}

.user-info span {
  margin-right: 15px;
}

.el-main {
  padding: 20px;
  background-color: #f5f7fa;
  overflow-y: auto;
}

.el-footer {
  background-color: #f5f7fa;
  color: #606266;
  text-align: center;
  line-height: 40px;
  border-top: 1px solid #dcdfe6;
}

.footer-content p {
  margin: 0;
  font-size: 12px;
}
</style> 