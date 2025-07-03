<template>
  <div class="summary-container">
    <div class="summary-card">
      <h1 class="summary-title">火眼金睛 - 挑战总结</h1>
      
      <p class="summary-thankyou">感谢您参与挑战！希望这次的经历能帮助您更好地识别网络中的钓鱼邮件。</p>
      
      <div v-if="loading" class="loading-spinner" v-loading="loading"></div>
      
      <el-alert v-if="error" :title="error" type="error" show-icon :closable="false" />
      
      <div v-if="summary && !loading" class="summary-content">
        <el-row :gutter="20" class="overall-stats">
          <el-col :span="8">
            <div class="stat-item">
              <div class="stat-value">{{ summary.total_correct }}</div>
              <div class="stat-label">总计正确</div>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="stat-item">
              <div class="stat-value">{{ summary.total_played }}</div>
              <div class="stat-label">总计判断</div>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="stat-item">
              <div class="stat-value primary">{{ accuracy }}%</div>
              <div class="stat-label">总体正确率</div>
            </div>
          </el-col>
        </el-row>
        
        <h2 class="level-title">各关卡战绩</h2>
        <el-table :data="summary.level_records" class="level-table" stripe>
          <el-table-column prop="level_name" label="关卡名称" min-width="150"></el-table-column>
          <el-table-column prop="correct_count" label="正确数" width="100" align="center"></el-table-column>
          <el-table-column prop="total_count" label="总数" width="100" align="center"></el-table-column>
          <el-table-column label="正确率" width="120" align="center">
            <template #default="scope">
              <span>{{ calculateLevelAccuracy(scope.row.correct_count, scope.row.total_count) }}%</span>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <div class="summary-actions">
        <el-button type="primary" @click="playAgain">再玩一次</el-button>
        <el-button @click="goHome">返回首页</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useGameStore } from '@/stores/game';
import { ElMessage } from 'element-plus';

const router = useRouter();
const gameStore = useGameStore();

const summary = computed(() => gameStore.summary);
const loading = computed(() => gameStore.loading);
const error = computed(() => gameStore.error);

const accuracy = computed(() => {
  if (!summary.value || summary.value.total_played === 0) {
    return 0;
  }
  return ((summary.value.total_correct / summary.value.total_played) * 100).toFixed(0);
});

const calculateLevelAccuracy = (correct, total) => {
  if (total === 0) return 0;
  return ((correct / total) * 100).toFixed(0);
};

onMounted(async () => {
  const { success, message } = await gameStore.fetchGameSummary();
  if (!success) {
    ElMessage.error(message);
  }
});

const playAgain = () => {
  router.push('/game/levels');
};

const goHome = () => {
  router.push('/');
};
</script>

<style scoped>
.summary-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 60px); /* 减去header高度 */
  background-color: #f5f7fa;
  padding: 20px;
}

.summary-card {
  max-width: 800px;
  width: 100%;
  background: #fff;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.summary-title {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 16px;
}

.summary-thankyou {
  font-size: 16px;
  color: #606266;
  margin-bottom: 32px;
}

.loading-spinner {
  height: 200px;
}

.overall-stats {
  margin-bottom: 32px;
}

.stat-item {
  padding: 20px;
  background-color: #fafafa;
  border-radius: 4px;
}

.stat-value {
  font-size: 36px;
  font-weight: bold;
  color: #303133;
}

.stat-value.primary {
  color: #409eff;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.level-title {
  font-size: 20px;
  margin-bottom: 16px;
  border-top: 1px solid #e4e7ed;
  padding-top: 32px;
}

.level-table {
  margin-bottom: 32px;
}

.summary-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
}
</style> 