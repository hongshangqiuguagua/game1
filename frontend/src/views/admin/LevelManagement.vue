<template>
  <div class="level-management-container">
    <h1 class="page-title">关卡管理</h1>
    
    <div class="top-actions">
      <el-button type="primary" @click="openForm()" icon="Plus">新建关卡</el-button>
      <el-input 
        v-model="searchQuery" 
        placeholder="搜索关卡..." 
        class="search-input" 
        clearable 
        prefix-icon="Search"
      />
    </div>

    <el-card class="level-table-card">
      <template #header>
        <div class="card-header">
          <h3>关卡列表</h3>
          <el-tag type="info">总计: {{ levels.length }} 个关卡</el-tag>
        </div>
      </template>
      
      <el-table 
        :data="filteredLevels" 
        v-loading="loading" 
        style="width: 100%"
        border
        stripe
        highlight-current-row
        empty-text="暂无关卡，请添加"
      >
        <el-table-column prop="order" label="顺序" width="80" sortable align="center"></el-table-column>
        <el-table-column prop="name" label="关卡名称" min-width="150" show-overflow-tooltip></el-table-column>
        <el-table-column prop="description" label="描述" min-width="250" show-overflow-tooltip></el-table-column>
        <el-table-column label="操作" width="250" align="center">
          <template #default="scope">
            <el-button-group>
              <el-button size="small" type="primary" @click="openForm(scope.row)" icon="Edit">
                编辑
              </el-button>
              <el-button size="small" type="success" @click="manageEmails(scope.row.id)" icon="Message">
                管理邮件
              </el-button>
              <el-button size="small" type="danger" @click="handleDelete(scope.row.id)" icon="Delete">
                删除
              </el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新建/编辑关卡弹窗 -->
    <el-dialog 
      v-model="formVisible" 
      :title="formTitle" 
      width="60%"
      destroy-on-close
      top="5vh"
    >
      <el-form 
        :model="currentLevel" 
        :rules="rules" 
        ref="levelForm" 
        label-width="120px"
        label-position="top"
      >
        <el-row :gutter="20">
          <el-col :span="16">
            <el-form-item label="关卡名称" prop="name">
              <el-input v-model="currentLevel.name" placeholder="请输入关卡名称"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="关卡顺序" prop="order">
              <el-input-number v-model="currentLevel.order" :min="1" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="关卡描述" prop="description">
          <el-input 
            type="textarea" 
            v-model="currentLevel.description" 
            :rows="3"
            placeholder="请输入关卡描述，这将显示给玩家"
          ></el-input>
        </el-form-item>
        
        <el-form-item label="本关总结" prop="trick_summary">
          <el-input 
            type="textarea" 
            v-model="currentLevel.trick_summary" 
            :rows="5" 
            placeholder="对本关所有钓鱼邮件的技巧进行一个总体归纳和总结，这将在玩家完成关卡后显示"
          ></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="formVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">
            {{ isEdit ? '保存修改' : '创建关卡' }}
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useAdminStore } from '@/stores/admin';
import { ElMessage, ElMessageBox } from 'element-plus';
import { useRouter } from 'vue-router';

const adminStore = useAdminStore();
const router = useRouter();
const levels = computed(() => adminStore.levels);
const loading = computed(() => adminStore.loading);
const searchQuery = ref('');
const submitting = ref(false);

const formVisible = ref(false);
const isEdit = ref(false);
const currentLevel = ref({});
const levelForm = ref(null);

const formTitle = computed(() => (isEdit.value ? '编辑关卡' : '新建关卡'));

// 过滤后的关卡列表
const filteredLevels = computed(() => {
  if (!searchQuery.value) return levels.value;
  
  const query = searchQuery.value.toLowerCase();
  return levels.value.filter(level => 
    level.name.toLowerCase().includes(query) || 
    level.description.toLowerCase().includes(query)
  );
});

const rules = {
  name: [{ required: true, message: '请输入关卡名称', trigger: 'blur' }],
  order: [{ required: true, message: '请输入关卡顺序', trigger: 'blur' }],
  description: [{ required: true, message: '请输入关卡描述', trigger: 'blur' }],
  trick_summary: [{ required: true, message: '请输入本关总结', trigger: 'blur' }],
};

const fetchLevels = async () => {
  const { success, message } = await adminStore.fetchLevels();
  if (!success) {
    ElMessage.error(message);
  }
};

onMounted(fetchLevels);

const openForm = (level = null) => {
  if (level) {
    isEdit.value = true;
    currentLevel.value = { ...level };
  } else {
    isEdit.value = false;
    currentLevel.value = { name: '', description: '', order: 1, trick_summary: '' };
  }
  formVisible.value = true;
};

const handleSubmit = async () => {
  if (!levelForm.value) return;
  
  try {
    await levelForm.value.validate();
    submitting.value = true;
    
    const action = isEdit.value ? adminStore.updateLevel : adminStore.createLevel;
    const { success, message, data } = await action(currentLevel.value);
    
    if (success) {
      ElMessage.success(isEdit.value ? '关卡更新成功' : '关卡创建成功');
      formVisible.value = false;
      await fetchLevels();
      
      // 如果是新建关卡，跳转到邮件管理页面
      if (!isEdit.value && data && data.id) {
        ElMessageBox.confirm(
          '关卡创建成功，是否立即添加邮件？',
          '提示',
          {
            confirmButtonText: '去添加邮件',
            cancelButtonText: '稍后再说',
            type: 'success'
          }
        ).then(() => {
          manageEmails(data.id);
        }).catch(() => {
          // 用户选择稍后再说，不做任何操作
        });
      }
    } else {
      ElMessage.error(message);
    }
  } catch (error) {
    console.error('提交失败:', error);
    ElMessage.error('提交失败: ' + (error.message || '未知错误'));
  } finally {
    submitting.value = false;
  }
};

// 管理关卡邮件
const manageEmails = (levelId) => {
  router.push({ name: 'AdminEmails', params: { levelId } });
};

const handleDelete = (id) => {
  ElMessageBox.confirm('确定要删除这个关卡吗？其下的所有邮件也将被删除。', '警告', {
    confirmButtonText: '确定删除',
    cancelButtonText: '取消',
    type: 'warning',
    confirmButtonClass: 'el-button--danger'
  }).then(async () => {
    loading.value = true;
    try {
      const { success, message } = await adminStore.deleteLevel(id);
      if (success) {
        ElMessage.success('删除成功');
        fetchLevels();
      } else {
        ElMessage.error(message);
      }
    } catch (error) {
      ElMessage.error('删除失败: ' + (error.message || '未知错误'));
    } finally {
      loading.value = false;
    }
  }).catch(() => {
    // 用户取消删除，不做任何操作
  });
};
</script>

<style scoped>
.level-management-container {
  padding: 24px;
}

.page-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #303133;
}

.top-actions {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.search-input {
  width: 300px;
}

.level-table-card {
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

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>