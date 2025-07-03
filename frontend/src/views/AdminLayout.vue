<template>
  <div class="admin-layout">
    <el-container>
      <el-aside width="200px">
        <div class="logo">
          <h3>管理后台</h3>
        </div>
        <el-menu
          router
          :default-active="activeMenu"
          class="el-menu-vertical"
          background-color="#304156"
          text-color="#bfcbd9"
          active-text-color="#409eff"
        >
          <el-menu-item index="/admin/levels">
            <el-icon><el-icon-menu></el-icon-menu></el-icon>
            <span>关卡管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/statistics">
            <el-icon><el-icon-data-analysis></el-icon-data-analysis></el-icon>
            <span>数据统计</span>
          </el-menu-item>
          <el-menu-item index="/game/levels">
            <el-icon><el-icon-back></el-icon-back></el-icon>
            <span>返回游戏</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <el-container>
        <el-header height="60px">
          <div class="header-content">
            <div class="breadcrumb">
              <el-breadcrumb separator="/">
                <el-breadcrumb-item :to="{ path: '/admin' }">管理后台</el-breadcrumb-item>
                <el-breadcrumb-item v-if="currentPath.includes('levels')">关卡管理</el-breadcrumb-item>
                <el-breadcrumb-item v-else-if="currentPath.includes('emails')">邮件管理</el-breadcrumb-item>
                <el-breadcrumb-item v-else-if="currentPath.includes('statistics')">数据统计</el-breadcrumb-item>
              </el-breadcrumb>
            </div>
            <div class="user-info">
              <span>{{ user?.username }}</span>
              <el-dropdown @command="handleCommand">
                <el-button icon="el-icon-setting" circle></el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>
        </el-header>
        
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { computed, ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'AdminLayout',
  
  setup() {
    const router = useRouter()
    const route = useRoute()
    const authStore = useAuthStore()
    
    // 获取当前用户
    const user = computed(() => authStore.getUser)
    
    // 获取当前路径
    const currentPath = ref(route.path)
    
    // 获取当前激活的菜单
    const activeMenu = computed(() => {
      if (route.path.includes('/admin/emails')) {
        return '/admin/levels'
      }
      return route.path
    })
    
    // 监听路由变化
    watch(() => route.path, (newPath) => {
      currentPath.value = newPath
    })
    
    // 下拉菜单命令处理
    const handleCommand = (command) => {
      if (command === 'logout') {
        ElMessageBox.confirm('确定要退出登录吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          authStore.logout()
          router.push('/')
        }).catch(() => {})
      }
    }
    
    return {
      user,
      currentPath,
      activeMenu,
      handleCommand
    }
  }
}
</script>

<style scoped>
.admin-layout {
  height: 100vh;
}

.el-container {
  height: 100%;
}

.el-aside {
  background-color: #304156;
  color: #bfcbd9;
}

.logo {
  height: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #fff;
  font-size: 16px;
  background-color: #263445;
}

.logo h3 {
  margin: 0;
}

.el-menu {
  border-right: none;
}

.el-header {
  background-color: #fff;
  color: #303133;
  line-height: 60px;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
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
</style> 