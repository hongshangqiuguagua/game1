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
                <el-button type="primary" @click.stop="selectLevel(level)">开始挑战</el-button>
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
}

.page-title {
  text-align: center;
  margin-bottom: 30px;
  color: #303133;
}

.level-list {
  margin-top: 20px;
}

.level-card {
  margin-bottom: 20px;
  cursor: pointer;
  transition: transform 0.3s;
}

.level-card:hover {
  transform: translateY(-5px);
}

.level-card-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
}

.level-icon {
  font-size: 40px;
  color: #409eff;
  margin-bottom: 15px;
}

.level-name {
  font-size: 18px;
  margin: 0 0 10px;
  color: #303133;
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
}

.error-message {
  margin-top: 20px;
}
</style> 