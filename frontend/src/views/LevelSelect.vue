<template>
  <div class="level-select-container">    
    <h1 class="page-title">选择挑战关卡</h1>
    
    <div class="level-list" v-loading="loading">
      <el-empty v-if="levels.length === 0 && !loading" description="暂无关卡"></el-empty>
      
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="level in levels" :key="level.id">
          <el-card class="level-card" shadow="hover" @click="selectLevel(level)">
            <div class="level-card-content">
              <div class="level-icon">
                <el-icon><el-icon-collection /></el-icon>
              </div>
              <h3 class="level-name">{{ level.name }}</h3>
              <p class="level-description">{{ level.description }}</p>
              <div class="level-footer">
                <el-button type="primary" class="play-button" @click.stop="selectLevel(level)">开始挑战</el-button>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    
    <div v-if="error" class="error-message">
      <el-alert
        :title="error"
        type="error"
        :closable="false"
        show-icon
      ></el-alert>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useGameStore } from '@/stores/game'

export default {
  name: 'LevelSelect',
  
  setup() {
    const router = useRouter()
    const gameStore = useGameStore()
    
    const levels = ref([])
    const loading = ref(false)
    const error = ref('')
    
    // 获取所有关卡
    const fetchLevels = async () => {
      loading.value = true
      error.value = ''
      
      try {
        const result = await gameStore.fetchLevels()
        
        if (result.success) {
          levels.value = result.levels
        } else {
          error.value = result.message
        }
      } catch (err) {
        console.error('获取关卡失败:', err)
        error.value = '获取关卡失败，请稍后再试'
      } finally {
        loading.value = false
      }
    }
    
    // 选择关卡
    const selectLevel = (level) => {
      router.push(`/game/play/${level.id}`)
    }
    
    // 组件挂载时获取关卡
    onMounted(() => {
      fetchLevels()
    })
    
    return {
      levels,
      loading,
      error,
      selectLevel
    }
  }
}
</script>

<style scoped>
.level-select-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  min-height: 100vh;
  position: relative;
  background: transparent;
  z-index: 1;
}

.page-title {
  text-align: center;
  margin-bottom: 30px;
  color: #303133;
  position: relative;
  z-index: 1;
  animation: fadeInUp 0.8s ease-out;
}

.page-title::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 3px;
  background-color: #409eff;
  animation: expandWidth 1s ease-out forwards;
}

@keyframes expandWidth {
  from { width: 0; }
  to { width: 100px; }
}

.level-list {
  margin-top: 30px;
  position: relative;
  z-index: 1;
}

.level-card {
  margin-bottom: 20px;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border-radius: 10px;
  overflow: hidden;
  background-color: #ffffff;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  animation: fadeInUp 0.8s ease-out;
  animation-fill-mode: both;
}

.level-card:nth-child(2n) {
  animation-delay: 0.2s;
}

.level-card:nth-child(3n) {
  animation-delay: 0.4s;
}

.level-card:nth-child(4n) {
  animation-delay: 0.6s;
}

.level-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
}

.level-card-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.level-icon {
  font-size: 50px;
  color: #409eff;
  margin-bottom: 20px;
  transition: all 0.3s ease;
  animation: floatIcon 3s ease-in-out infinite;
}

@keyframes floatIcon {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.level-card:hover .level-icon {
  transform: scale(1.2);
  color: #66b1ff;
}

.level-name {
  font-size: 20px;
  margin: 0 0 15px;
  color: #303133;
  position: relative;
  padding-bottom: 10px;
}

.level-name::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 30px;
  height: 2px;
  background-color: #409eff;
  transition: width 0.3s ease;
}

.level-card:hover .level-name::after {
  width: 50px;
}

.level-description {
  text-align: center;
  color: #606266;
  margin-bottom: 20px;
  height: 60px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.level-footer {
  width: 100%;
  text-align: center;
  margin-top: auto;
}

.play-button {
  padding: 12px 25px;
  font-size: 16px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  border-radius: 25px;
}

.play-button::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.play-button:hover::after {
  left: 100%;
}

.error-message {
  margin-top: 20px;
  position: relative;
  z-index: 1;
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
</style> 