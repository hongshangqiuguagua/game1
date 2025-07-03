<template>
  <div class="statistics-container">
    <h1 class="page-title">邮件错误率统计</h1>
    <p class="page-description">
      这里展示了每封邮件被玩家判断错误的情况。错误率越高，说明该邮件的设计越具有迷惑性，值得关注。
      这些数据可以帮助您优化关卡设计和邮件内容。
    </p>
    
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="6" animated />
    </div>
    
    <el-alert v-if="error" :title="error" type="error" show-icon :closable="false" style="margin-bottom: 20px;" />
    
    <div v-if="!loading && !error">
      <div class="stats-summary">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card shadow="hover" class="summary-card">
              <div class="summary-item">
                <div class="summary-icon">
                  <el-icon><DataLine /></el-icon>
                </div>
                <div class="summary-content">
                  <div class="summary-title">总邮件数</div>
                  <div class="summary-value">{{ emailStats.length }}</div>
                </div>
              </div>
            </el-card>
          </el-col>
          
          <el-col :span="8">
            <el-card shadow="hover" class="summary-card">
              <div class="summary-item">
                <div class="summary-icon warning">
                  <el-icon><Warning /></el-icon>
                </div>
                <div class="summary-content">
                  <div class="summary-title">高错误率邮件</div>
                  <div class="summary-value">{{ highErrorRateEmails.length }}</div>
                  <div class="summary-subtitle">错误率 > 50%</div>
                </div>
              </div>
            </el-card>
          </el-col>
          
          <el-col :span="8">
            <el-card shadow="hover" class="summary-card">
              <div class="summary-item">
                <div class="summary-icon success">
                  <el-icon><SuccessFilled /></el-icon>
                </div>
                <div class="summary-content">
                  <div class="summary-title">低错误率邮件</div>
                  <div class="summary-value">{{ lowErrorRateEmails.length }}</div>
                  <div class="summary-subtitle">错误率 < 20%</div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
      
      <div class="filter-bar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索邮件..."
          prefix-icon="Search"
          clearable
          style="width: 300px;"
        />
        
        <el-select v-model="typeFilter" placeholder="邮件类型" clearable style="width: 150px; margin-left: 10px;">
          <el-option label="全部" value="" />
          <el-option label="钓鱼邮件" value="phishing" />
          <el-option label="正常邮件" value="normal" />
        </el-select>
        
        <el-select v-model="sortBy" placeholder="排序方式" style="width: 150px; margin-left: 10px;">
          <el-option label="错误率 (高到低)" value="error_rate_desc" />
          <el-option label="错误率 (低到高)" value="error_rate_asc" />
          <el-option label="判断次数 (多到少)" value="judgement_count_desc" />
        </el-select>
      </div>
      
      <div class="stats-table">
        <el-card>
          <template #header>
            <div class="card-header">
              <h3>邮件错误率详情</h3>
              <div class="header-actions">
                <el-tooltip content="刷新数据" placement="top">
                  <el-button circle @click="refreshData" :loading="loading" icon="Refresh"></el-button>
                </el-tooltip>
              </div>
            </div>
          </template>
          
          <el-table 
            :data="filteredEmailStats" 
            style="width: 100%" 
            stripe 
            border
            :row-class-name="tableRowClassName"
            empty-text="暂无数据，请先让玩家体验游戏"
          >
            <el-table-column prop="subject" label="邮件主题" min-width="250" show-overflow-tooltip>
              <template #default="scope">
                <div class="email-subject">
                  <el-icon v-if="scope.row.is_phishing" class="warning-icon" color="#F56C6C"><WarningFilled /></el-icon>
                  <span>{{ scope.row.subject }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="sender" label="发件人" min-width="200" show-overflow-tooltip></el-table-column>
            <el-table-column prop="is_phishing" label="邮件类型" width="120" align="center">
              <template #default="scope">
                <el-tag :type="scope.row.is_phishing ? 'danger' : 'success'">
                  {{ scope.row.is_phishing ? '钓鱼邮件' : '正常邮件' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="judgement_count" label="总判断次数" width="120" align="center"></el-table-column>
            <el-table-column prop="error_count" label="错误次数" width="120" align="center"></el-table-column>
            <el-table-column label="错误率" width="180" align="center">
              <template #default="scope">
                <div class="error-rate-container">
                  <el-progress 
                    :percentage="scope.row.error_rate" 
                    :color="getErrorRateColor(scope.row.error_rate)"
                    :stroke-width="16"
                    :format="() => scope.row.error_rate.toFixed(2) + '%'"
                  ></el-progress>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
        
        <div class="tips-section">
          <el-alert
            title="数据解读提示"
            type="info"
            description="错误率高的邮件表示玩家难以正确判断，可能需要调整难度或增加提示。错误率接近0的邮件可能太容易被识别，考虑增加一些迷惑性。"
            :closable="false"
            show-icon
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useAdminStore } from '@/stores/admin';
import { ElMessage } from 'element-plus';
import { DataLine, Warning, SuccessFilled, WarningFilled } from '@element-plus/icons-vue';

const adminStore = useAdminStore();

const emailStats = computed(() => adminStore.emailStats || []);
const loading = computed(() => adminStore.loading);
const error = computed(() => adminStore.error);

const searchQuery = ref('');
const typeFilter = ref('');
const sortBy = ref('error_rate_desc');

// 计算属性：高错误率邮件
const highErrorRateEmails = computed(() => 
  emailStats.value.filter(email => email.error_rate > 50)
);

// 计算属性：低错误率邮件
const lowErrorRateEmails = computed(() => 
  emailStats.value.filter(email => email.error_rate < 20)
);

// 过滤和排序后的邮件列表
const filteredEmailStats = computed(() => {
  // 1. 应用搜索过滤
  let filtered = emailStats.value;
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(email => 
      email.subject.toLowerCase().includes(query) || 
      email.sender.toLowerCase().includes(query)
    );
  }
  
  // 2. 应用类型过滤
  if (typeFilter.value === 'phishing') {
    filtered = filtered.filter(email => email.is_phishing);
  } else if (typeFilter.value === 'normal') {
    filtered = filtered.filter(email => !email.is_phishing);
  }
  
  // 3. 应用排序
  if (sortBy.value === 'error_rate_desc') {
    filtered = [...filtered].sort((a, b) => b.error_rate - a.error_rate);
  } else if (sortBy.value === 'error_rate_asc') {
    filtered = [...filtered].sort((a, b) => a.error_rate - b.error_rate);
  } else if (sortBy.value === 'judgement_count_desc') {
    filtered = [...filtered].sort((a, b) => b.judgement_count - a.judgement_count);
  }
  
  return filtered;
});

// 获取错误率颜色
const getErrorRateColor = (rate) => {
  if (rate > 70) return '#F56C6C'; // 高错误率 - 红色
  if (rate > 50) return '#E6A23C'; // 中高错误率 - 橙色
  if (rate > 30) return '#409EFF'; // 中等错误率 - 蓝色
  return '#67C23A'; // 低错误率 - 绿色
};

// 表格行样式
const tableRowClassName = ({ row }) => {
  if (row.error_rate > 70) {
    return 'error-row-high';
  }
  if (row.error_rate > 50) {
    return 'error-row-medium';
  }
  return '';
};

// 刷新数据
const refreshData = async () => {
  try {
    const { success, message } = await adminStore.fetchEmailStats();
    if (!success) {
      ElMessage.error(message || '获取数据失败');
    } else {
      ElMessage.success('数据已刷新');
    }
  } catch (error) {
    ElMessage.error('刷新数据时发生错误');
    console.error('刷新数据错误:', error);
  }
};

onMounted(async () => {
  await refreshData();
});
</script>

<style scoped>
.statistics-container {
  padding: 24px;
}

.page-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 8px;
  color: #303133;
}

.page-description {
  font-size: 14px;
  color: #606266;
  margin-bottom: 24px;
  max-width: 800px;
  line-height: 1.6;
}

.loading-container {
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 4px;
  margin-bottom: 20px;
}

.stats-summary {
  margin-bottom: 24px;
}

.summary-card {
  height: 100%;
}

.summary-item {
  display: flex;
  align-items: center;
}

.summary-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background-color: #409EFF;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  color: white;
  font-size: 24px;
}

.summary-icon.warning {
  background-color: #E6A23C;
}

.summary-icon.success {
  background-color: #67C23A;
}

.summary-content {
  flex: 1;
}

.summary-title {
  font-size: 14px;
  color: #606266;
  margin-bottom: 4px;
}

.summary-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.summary-subtitle {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.filter-bar {
  display: flex;
  margin-bottom: 20px;
}

.stats-table {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 18px;
}

.email-subject {
  display: flex;
  align-items: center;
  gap: 5px;
}

.warning-icon {
  font-size: 16px;
}

.error-rate-container {
  width: 100%;
}

:deep(.el-table .error-row-high) {
  background-color: rgba(245, 108, 108, 0.1) !important;
}

:deep(.el-table .error-row-medium) {
  background-color: rgba(230, 162, 60, 0.1) !important;
}

.tips-section {
  margin-top: 20px;
}
</style>