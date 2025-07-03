<template>
  <div class="email-management">
    <el-page-header @back="goBack" :title="`返回关卡管理`" :content="`邮件管理 - ${levelName}`" />
    
    <div class="email-management-content">
      <div class="top-actions">
        <el-button type="primary" @click="openEmailDialog()" icon="Plus">新建邮件</el-button>
        <el-input 
          v-model="searchQuery" 
          placeholder="搜索邮件..." 
          class="search-input" 
          clearable 
          prefix-icon="Search"
        />
      </div>
      
      <el-card class="email-table-card">
        <template #header>
          <div class="card-header">
            <h3>邮件列表</h3>
            <div class="email-stats">
              <el-tag type="info">总计: {{ emails.length }}</el-tag>
              <el-tag type="danger">钓鱼邮件: {{ phishingCount }}</el-tag>
              <el-tag type="success">正常邮件: {{ normalCount }}</el-tag>
            </div>
          </div>
        </template>
        
        <el-table 
          :data="filteredEmails" 
          v-loading="loading" 
          style="width: 100%"
          border
          stripe
          highlight-current-row
          empty-text="暂无邮件，请添加"
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
          <el-table-column prop="is_phishing" label="类型" width="120" align="center">
            <template #default="scope">
              <el-tag :type="scope.row.is_phishing ? 'danger' : 'success'">
                {{ scope.row.is_phishing ? '钓鱼邮件' : '正常邮件' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" align="center">
            <template #default="scope">
              <el-button-group>
                <el-button size="small" type="primary" @click="openEmailDialog(scope.row)" icon="Edit">
                  编辑
                </el-button>
                <el-button size="small" type="danger" @click="handleDelete(scope.row.id)" icon="Delete">
                  删除
                </el-button>
              </el-button-group>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>

    <!-- 新建/编辑邮件弹窗 -->
    <el-dialog 
      v-model="dialogVisible" 
      :title="isEdit ? '编辑邮件' : '新建邮件'" 
      width="60%" 
      destroy-on-close
      top="5vh"
    >
      <el-form 
        :model="currentEmail" 
        :rules="formRules" 
        ref="emailForm" 
        label-width="120px"
        label-position="top"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="发件人" prop="sender">
              <el-input v-model="currentEmail.sender" placeholder="请输入发件人邮箱地址"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="邮件主题" prop="subject">
              <el-input v-model="currentEmail.subject" placeholder="请输入邮件主题"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="邮件内容" prop="content">
          <el-input 
            type="textarea" 
            :rows="10" 
            v-model="currentEmail.content" 
            placeholder="请输入邮件内容"
          ></el-input>
        </el-form-item>
        
        <el-form-item label="邮件类型">
          <el-radio-group v-model="currentEmail.is_phishing">
            <el-radio :label="false">正常邮件</el-radio>
            <el-radio :label="true">钓鱼邮件</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item v-if="currentEmail.is_phishing" label="骗术揭秘" prop="phishing_clue">
          <el-input 
            type="textarea" 
            :rows="4" 
            v-model="currentEmail.phishing_clue" 
            placeholder="请描述这封钓鱼邮件的骗术特征，以便在游戏结束时向玩家展示"
          ></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleConfirm" :loading="submitting">
            {{ isEdit ? '保存修改' : '创建邮件' }}
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, reactive } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAdminStore } from '@/stores/admin';
import { ElMessage, ElMessageBox } from 'element-plus';
import { WarningFilled } from '@element-plus/icons-vue';

const route = useRoute();
const router = useRouter();
const adminStore = useAdminStore();

const levelId = computed(() => route.params.levelId);
const emails = ref([]);
const loading = ref(true);
const submitting = ref(false);
const searchQuery = ref('');
const levelName = ref('');

const dialogVisible = ref(false);
const isEdit = ref(false);
const currentEmail = ref({});
const emailForm = ref(null);

// 表单验证规则
const formRules = {
  sender: [
    { required: true, message: '请输入发件人', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ],
  subject: [
    { required: true, message: '请输入邮件主题', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入邮件内容', trigger: 'blur' }
  ],
  phishing_clue: [
    { required: true, message: '请输入骗术揭秘', trigger: 'blur' }
  ]
};

// 计算属性：过滤后的邮件列表
const filteredEmails = computed(() => {
  if (!searchQuery.value) return emails.value;
  
  const query = searchQuery.value.toLowerCase();
  return emails.value.filter(email => 
    email.subject.toLowerCase().includes(query) || 
    email.sender.toLowerCase().includes(query)
  );
});

// 计算钓鱼邮件和正常邮件的数量
const phishingCount = computed(() => emails.value.filter(email => email.is_phishing).length);
const normalCount = computed(() => emails.value.filter(email => !email.is_phishing).length);

// 返回关卡管理页面
const goBack = () => {
  router.push({ name: 'AdminLevels' });
};

const resetCurrentEmail = () => {
  currentEmail.value = {
    level_id: parseInt(levelId.value, 10),
    sender: '',
    subject: '',
    content: '',
    is_phishing: false,
    phishing_clue: ''
  };
};

const fetchLevelInfo = async () => {
  try {
    const response = await adminStore.fetchLevels();
    if (response.success && response.levels) {
      const level = response.levels.find(l => l.id === parseInt(levelId.value));
      if (level) {
        levelName.value = level.name;
      } else {
        levelName.value = `关卡 ${levelId.value}`;
      }
    }
  } catch (error) {
    console.error('获取关卡信息失败:', error);
    levelName.value = `关卡 ${levelId.value}`;
  }
};

const fetchEmails = async () => {
  loading.value = true;
  try {
    const result = await adminStore.fetchLevelEmails(levelId.value);
    emails.value = Array.isArray(result) ? result : [];
  } catch (error) {
    ElMessage.error('获取邮件列表失败');
    emails.value = [];
  } finally {
    loading.value = false;
  }
};

const openEmailDialog = (email = null) => {
  if (email) {
    isEdit.value = true;
    currentEmail.value = { ...email };
  } else {
    isEdit.value = false;
    resetCurrentEmail();
  }
  dialogVisible.value = true;
};

const handleConfirm = async () => {
  if (!emailForm.value) return;
  
  try {
    await emailForm.value.validate();
    submitting.value = true;
    
    // 确保钓鱼邮件有骗术揭秘
    if (currentEmail.value.is_phishing && !currentEmail.value.phishing_clue) {
      ElMessage.warning('请为钓鱼邮件添加骗术揭秘');
      return;
    }
    
    if (isEdit.value) {
      await adminStore.updateEmail(currentEmail.value.id, currentEmail.value);
      ElMessage.success('邮件更新成功');
    } else {
      await adminStore.createEmail(currentEmail.value);
      ElMessage.success('邮件创建成功');
    }
    
    dialogVisible.value = false;
    await fetchEmails();
  } catch (error) {
    console.error('操作失败:', error);
    ElMessage.error('操作失败: ' + (error.response?.data?.detail || error.message || '未知错误'));
  } finally {
    submitting.value = false;
  }
};

const handleDelete = async (emailId) => {
  try {
    await ElMessageBox.confirm('确定要删除这封邮件吗？此操作不可恢复。', '警告', {
      confirmButtonText: '确定删除',
      cancelButtonText: '取消',
      type: 'warning',
      confirmButtonClass: 'el-button--danger'
    });
    
    loading.value = true;
    await adminStore.deleteEmail(emailId);
    ElMessage.success('邮件删除成功');
    await fetchEmails();
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error);
      ElMessage.error('删除失败: ' + (error.response?.data?.detail || error.message || '未知错误'));
    }
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  await fetchLevelInfo();
  await fetchEmails();
});
</script>

<style scoped>
.email-management {
  padding: 20px;
}

.email-management-content {
  margin-top: 20px;
}

.top-actions {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.search-input {
  width: 300px;
}

.email-table-card {
  margin-bottom: 20px;
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

.email-stats {
  display: flex;
  gap: 10px;
}

.email-subject {
  display: flex;
  align-items: center;
  gap: 5px;
}

.warning-icon {
  font-size: 16px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style> 