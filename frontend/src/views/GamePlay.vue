<template>
  <div class="game-play-container" v-loading="loading">
    <!-- 顶部导航栏 - 模仿Outlook -->
    <div class="outlook-header">
      <div class="outlook-logo">
        <span>Outlook</span>
      </div>
      <div class="outlook-search">
        <el-input placeholder="搜索" prefix-icon="el-icon-search" disabled></el-input>
      </div>
      <div class="outlook-actions">
        <el-tooltip content="设置" placement="bottom">
          <el-icon class="header-icon"><el-icon-setting /></el-icon>
        </el-tooltip>
        <el-tooltip content="帮助" placement="bottom">
          <el-icon class="header-icon"><el-icon-question-filled /></el-icon>
        </el-tooltip>
        <el-tooltip content="这是游戏模拟界面" placement="bottom">
          <el-icon class="header-icon"><el-icon-info-filled /></el-icon>
        </el-tooltip>
        <div class="user-avatar">{{ getCurrentUserInitial() }}</div>
      </div>
    </div>
    
    <!-- 操作栏 - 模仿Outlook -->
    <div class="outlook-toolbar">
      <div class="toolbar-tabs">
        <div class="tab active">主页</div>
        <div class="tab">查看</div>
        <div class="tab">帮助</div>
      </div>
      <div class="toolbar-actions">
        <div class="action-group">
          <el-button type="primary" size="small" disabled>
            <el-icon><el-icon-plus /></el-icon>
            <span>新邮件</span>
          </el-button>
        </div>
        <div class="action-group">
          <el-button type="text" size="small" disabled>
            <el-icon><el-icon-delete /></el-icon>
            <span>删除</span>
          </el-button>
          <el-button type="text" size="small" disabled>
            <el-icon><el-icon-folder /></el-icon>
            <span>存档</span>
          </el-button>
          <el-button v-if="currentView === 'inbox'" type="warning" size="small" @click="identifyPhishingPrompt">
            <el-icon><el-icon-warning /></el-icon>
            <span>标记为钓鱼邮件</span>
          </el-button>
          <el-button v-else type="success" size="small" @click="switchView('inbox')">
            <el-icon><el-icon-back /></el-icon>
            <span>返回收件箱</span>
          </el-button>
        </div>
        
        <!-- 游戏操作按钮组 -->
        <div class="game-action-group">
          <el-button type="warning" @click="exitGame" :disabled="loading">退出游戏</el-button>
          <el-button type="primary" @click="submitLevel" :disabled="loading">完成本关</el-button>
        </div>
      </div>
    </div>
    
    <!-- 关卡信息提示 -->
    <div class="level-info-banner" v-if="currentLevel">
      <el-alert
        title="游戏任务"
        :description="currentLevel.description"
        type="info"
        show-icon
        :closable="false"
      />
    </div>
    
    <!-- 拖拽提示 -->
    <div class="drag-hint-banner">
      <el-alert
        v-if="currentView === 'inbox'"
        title="操作提示"
        description="您可以拖拽邮件到垃圾桶，或者点击邮件后使用删除按钮将可疑邮件移入垃圾桶"
        type="warning"
        show-icon
        :closable="false"
      />
      <el-alert
        v-else
        title="操作提示"
        description="您可以拖拽邮件到收件箱，或者点击邮件后使用恢复按钮将邮件恢复到收件箱"
        type="success"
        show-icon
        :closable="false"
      />
    </div>
    
    <div class="email-client" v-if="!loading">
      <div class="sidebar">
        <div class="folder-list">
          <div class="user-profile">
            <div class="avatar">{{ getCurrentUserInitial() }}</div>
            <div class="user-info">
              <div class="username">当前用户</div>
              <div class="email">user@example.com</div>
            </div>
          </div>
          
          <div class="folder-header">收藏夹</div>
          <div 
            class="folder" 
            :class="{ active: currentView === 'inbox', 'drag-over': isDragOverInbox }"
            data-folder="inbox"
            @click="switchView('inbox')"
            @dragover="handleDragOverInbox"
            @dragleave="handleDragLeaveInbox"
            @drop="handleDropToInbox"
          >
            <el-icon><el-icon-message /></el-icon>
            <span>收件箱</span>
            <span class="count" v-if="inboxEmails.length > 0">{{ inboxEmails.length }}</span>
          </div>
          <div class="folder">
            <el-icon><el-icon-star /></el-icon>
            <span>已加星标</span>
          </div>
          
          <div class="folder-header">文件夹</div>
          <div 
            class="folder" 
            :class="{ active: currentView === 'trash', 'drag-over': isDragOverTrash }" 
            data-folder="trash" 
            @click="switchView('trash')"
            @dragover="handleDragOverTrash" 
            @dragleave="handleDragLeaveTrash" 
            @drop="handleDropToTrash"
          >
            <el-icon><el-icon-delete /></el-icon>
            <span>垃圾桶</span>
            <span class="count" v-if="trashEmails.length > 0">{{ trashEmails.length }}</span>
          </div>
          <div class="folder">
            <el-icon><el-icon-position /></el-icon>
            <span>已发送</span>
          </div>
          <div class="folder">
            <el-icon><el-icon-document /></el-icon>
            <span>草稿</span>
          </div>
          <div class="folder">
            <el-icon><el-icon-folder /></el-icon>
            <span>存档</span>
          </div>
        </div>
      </div>
      
      <div class="email-content-wrapper">
        <div class="email-list-header">
          <div class="list-title">{{ currentView === 'inbox' ? '收件箱' : '垃圾桶' }}</div>
          <div class="list-actions">
            <el-tooltip content="刷新" placement="bottom">
              <el-icon class="action-icon"><el-icon-refresh /></el-icon>
            </el-tooltip>
            <el-tooltip content="排序" placement="bottom">
              <el-icon class="action-icon"><el-icon-sort /></el-icon>
            </el-tooltip>
            <el-tooltip content="更多操作" placement="bottom">
              <el-icon class="action-icon"><el-icon-more /></el-icon>
            </el-tooltip>
          </div>
        </div>
        
        <div class="email-list">
          <!-- 收件箱视图 -->
          <template v-if="currentView === 'inbox' && inboxEmails.length > 0">
            <TransitionGroup name="email-list" tag="div" class="email-list-container">
            <EmailItem
              v-for="email in inboxEmails"
              :key="email.id"
              :email="email"
              :is-read="isEmailRead(email.id)"
              :is-selected="selectedEmail && selectedEmail.id === email.id"
              @click="selectEmail(email.id)"
                @dragstart="handleDragStart($event, email.id)"
            />
            </TransitionGroup>
          </template>
          
          <!-- 垃圾箱视图 -->
          <template v-else-if="currentView === 'trash' && trashEmails.length > 0">
            <TransitionGroup name="email-list" tag="div" class="email-list-container">
              <EmailItem
                v-for="email in trashEmails"
                :key="email.id"
                :email="email"
                :is-read="isEmailRead(email.id)"
                :is-selected="selectedEmail && selectedEmail.id === email.id"
                :is-in-trash="true"
                @click="selectEmail(email.id)"
                @dragstart="handleDragStart($event, email.id)"
                @restore="restoreFromTrash"
              />
            </TransitionGroup>
          </template>
          
          <el-empty v-else :description="currentView === 'inbox' ? '收件箱为空' : '垃圾桶为空'"></el-empty>
      </div>
      
      <div class="content-area">
          <div v-if="selectedEmail" class="content-toolbar">
            <div class="toolbar-actions">
              <el-tooltip content="回复" placement="bottom">
                <div class="toolbar-button"><el-icon><el-icon-reply /></el-icon></div>
              </el-tooltip>
              <el-tooltip content="转发" placement="bottom">
                <div class="toolbar-button"><el-icon><el-icon-share /></el-icon></div>
              </el-tooltip>
              
              <!-- 根据当前视图显示不同的操作按钮 -->
              <template v-if="isSelectedEmailInTrash">
                <el-tooltip content="恢复邮件" placement="bottom">
                  <div class="toolbar-button highlight-button" @click="restoreCurrentEmail">
                    <el-icon><el-icon-top /></el-icon>
                  </div>
                </el-tooltip>
              </template>
              <template v-else>
                <el-tooltip content="移至垃圾桶" placement="bottom">
                  <div class="toolbar-button" @click="moveCurrentEmailToTrash">
                    <el-icon><el-icon-delete /></el-icon>
                  </div>
                </el-tooltip>
              </template>
            </div>
          </div>
        <EmailContent :email="selectedEmail" />
        </div>
      </div>
    </div>
    
    <!-- 关卡结果弹窗 -->
    <LevelResultModal
      v-if="gameResult"
      v-model:visible="resultModalVisible"
      :result="gameResult"
      :is-last-level="isLastLevel"
      @next-level="goToNextLevel"
      @view-summary="viewSummary"
      @go-to-levels="goToLevels"
    />
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useGameStore } from '@/stores/game'
import { useAuthStore } from '@/stores/auth'
import EmailItem from '@/components/EmailItem.vue'
import EmailContent from '@/components/EmailContent.vue'
import TrashBin from '@/components/TrashBin.vue'
import LevelResultModal from '@/components/LevelResultModal.vue'

export default {
  name: 'GamePlay',
  
  components: {
    EmailItem,
    EmailContent,
    TrashBin,
    LevelResultModal
  },
  
  props: {
    levelId: {
      type: [String, Number],
      required: true
    }
  },
  
  setup(props) {
    const route = useRoute()
    const router = useRouter()
    const gameStore = useGameStore()
    const authStore = useAuthStore()
    
    const loading = ref(false)
    const resultModalVisible = ref(false)
    const isDragOverTrash = ref(false)
    const isDragOverInbox = ref(false)
    const currentView = ref('inbox') // 新增：当前视图（收件箱或垃圾桶）
    
    // 计算属性
    const currentLevel = computed(() => gameStore.getCurrentLevel)
    const inboxEmails = computed(() => gameStore.getInboxEmails)
    const trashEmails = computed(() => gameStore.getTrashEmails)
    const selectedEmail = computed(() => gameStore.getSelectedEmail)
    const gameResult = computed(() => gameStore.getGameResult)
    const isLastLevel = computed(() => {
      if (!gameResult.value) return false
      return !gameResult.value.next_level_id
    })
    
    // 判断当前选中的邮件是否在垃圾桶中
    const isSelectedEmailInTrash = computed(() => {
      if (!selectedEmail.value) return false;
      return gameStore.isEmailInTrash(selectedEmail.value.id);
    });
    
    // 切换视图（收件箱/垃圾桶）
    const switchView = (view) => {
      currentView.value = view;
      // 取消当前选中的邮件
      gameStore.selectEmail(null);
    };
    
    // 获取当前用户名首字母
    const getCurrentUserInitial = () => {
      const user = authStore.getUser
      if (user && user.username) {
        return user.username.charAt(0).toUpperCase()
      }
      return 'U'
    }
    
    // 判断邮件是否已读
    const isEmailRead = (emailId) => {
      return gameStore.isEmailRead(emailId)
    }
    
    // 选择邮件
    const selectEmail = (emailId) => {
      gameStore.selectEmail(emailId)
    }
    
    // 处理邮件拖拽开始
    const handleDragStart = (event, emailId) => {
      console.log('开始拖拽邮件:', emailId);
      
      // 创建自定义拖拽图像
      if (event.dataTransfer) {
        // 设置拖拽数据
        event.dataTransfer.setData('text/plain', emailId);
        event.dataTransfer.effectAllowed = 'move';
        
        // 查找被拖拽的邮件元素
        const emailItem = event.currentTarget;
        if (emailItem) {
          // 克隆邮件元素作为拖拽图像
          const dragImage = emailItem.cloneNode(true);
          dragImage.style.width = `${emailItem.offsetWidth}px`;
          dragImage.style.backgroundColor = '#ffffff';
          dragImage.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.1)';
          dragImage.style.opacity = '0.9';
          dragImage.style.position = 'absolute';
          dragImage.style.top = '-1000px';
          dragImage.style.left = '0';
          dragImage.style.zIndex = '-1';
          document.body.appendChild(dragImage);
          
          // 设置拖拽图像
          event.dataTransfer.setDragImage(dragImage, 20, 20);
          
          // 在下一帧移除拖拽图像
          setTimeout(() => {
            document.body.removeChild(dragImage);
          }, 0);
        }
      }
    };
    
    // 垃圾桶拖拽处理
    const handleDragOverTrash = (event) => {
      event.preventDefault();
      event.dataTransfer.dropEffect = 'move';
      isDragOverTrash.value = true;
      
      const trashFolder = event.currentTarget;
      if (trashFolder && !trashFolder.classList.contains('pulse-animation')) {
        trashFolder.classList.add('pulse-animation');
      }
    };
    
    const handleDragLeaveTrash = (event) => {
      isDragOverTrash.value = false;
      
      const trashFolder = event.currentTarget;
      if (trashFolder) {
        trashFolder.classList.remove('pulse-animation');
      }
    };
    
    const handleDropToTrash = (event) => {
      event.preventDefault();
      isDragOverTrash.value = false;
      
      const trashFolder = event.currentTarget;
      if (trashFolder) {
        trashFolder.classList.remove('pulse-animation');
      }
      
      // 获取拖拽的邮件ID
      const emailId = event.dataTransfer.getData('text/plain');
      if (emailId) {
        moveToTrash(parseInt(emailId));
      }
    };
    
    // 收件箱拖拽处理
    const handleDragOverInbox = (event) => {
      // 如果当前视图是收件箱，不需要处理收件箱的拖拽事件
      if (currentView.value === 'inbox') return;
      
      event.preventDefault();
      event.dataTransfer.dropEffect = 'move';
      isDragOverInbox.value = true;
      
      const inboxFolder = event.currentTarget;
      if (inboxFolder && !inboxFolder.classList.contains('pulse-animation')) {
        inboxFolder.classList.add('pulse-animation');
      }
    };
    
    const handleDragLeaveInbox = (event) => {
      isDragOverInbox.value = false;
      
      const inboxFolder = event.currentTarget;
      if (inboxFolder) {
        inboxFolder.classList.remove('pulse-animation');
      }
    };
    
    const handleDropToInbox = (event) => {
      event.preventDefault();
      isDragOverInbox.value = false;
      
      const inboxFolder = event.currentTarget;
      if (inboxFolder) {
        inboxFolder.classList.remove('pulse-animation');
      }
      
      // 获取拖拽的邮件ID
      const emailId = event.dataTransfer.getData('text/plain');
      if (emailId) {
        restoreFromTrash(parseInt(emailId));
      }
    };
    
    // 将当前选中的邮件移至垃圾桶
    const moveCurrentEmailToTrash = () => {
      if (selectedEmail.value) {
        moveToTrash(selectedEmail.value.id);
      }
    };
    
    // 将邮件移入垃圾桶
    const moveToTrash = (emailId) => {
      gameStore.moveToTrash(emailId);
      
      // 添加震动效果给垃圾桶图标
      const trashFolder = document.querySelector('.folder[data-folder="trash"]');
      if (trashFolder) {
        trashFolder.classList.add('shake-animation');
        setTimeout(() => {
          trashFolder.classList.remove('shake-animation');
        }, 500);
      }
      
      ElMessage.success({
        message: '邮件已移至垃圾桶',
        duration: 1500,
        offset: 80
      });
    };
    
    // 从垃圾箱恢复邮件
    const restoreFromTrash = (emailId) => {
      gameStore.restoreFromTrash(emailId);
      
      ElMessage.success({
        message: '邮件已恢复至收件箱',
        duration: 1500,
        offset: 80
      });
    };
    
    // 从垃圾箱恢复当前选中的邮件
    const restoreCurrentEmail = () => {
      if (selectedEmail.value) {
        const emailId = selectedEmail.value.id;
        restoreFromTrash(emailId);
      }
    };
    
    // 提交关卡结果
    const submitLevel = async () => {
      ElMessageBox.confirm(
        '确定要完成本关吗？提交后将无法修改您的判断。',
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(async () => {
        loading.value = true
        
        try {
          // 准备判断结果数据
          const judgments = [];
          
          // 获取所有邮件（包括收件箱和垃圾箱中的邮件）
          const allEmails = [...inboxEmails.value, ...trashEmails.value];
          
          // 遍历所有邮件，记录用户的判断
          allEmails.forEach(email => {
            // 如果邮件在垃圾箱中，说明用户判断它是钓鱼邮件
            // 如果邮件在收件箱中，说明用户判断它不是钓鱼邮件
            const isInTrash = gameStore.isEmailInTrash(email.id);
            judgments.push({
              email_id: email.id,
              is_phishing_guess: isInTrash
            });
          });
          
          console.log('提交判断结果:', judgments);
          
          // 提交判断结果
          const response = await gameStore.submitLevel(props.levelId, judgments);
          
          if (response.success) {
            // 显示结算弹窗
            resultModalVisible.value = true;
          } else {
            ElMessage.error(response.message || '提交关卡失败');
          }
        } catch (error) {
          console.error('提交关卡失败:', error);
          ElMessage.error('提交关卡失败，请稍后再试');
        } finally {
          loading.value = false;
        }
      }).catch(() => {
        // 用户取消操作
      });
    }
    
    // 前往下一关
    const goToNextLevel = (nextLevelId) => {
      if (nextLevelId) {
        router.push(`/game/play/${nextLevelId}`)
      } else {
        router.push('/game/levels')
      }
    }
    
    // 查看总结
    const viewSummary = () => {
      router.push('/summary')
    }
    
    // 退出游戏
    const exitGame = () => {
      ElMessageBox.confirm(
        '确定要退出当前游戏吗？未保存的进度将会丢失。',
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(() => {
        gameStore.resetGameState()
        router.push('/game/levels')
      }).catch(() => {})
    }
    
    // 加载关卡数据
    const loadLevelData = async () => {
      loading.value = true
      
      try {
        const result = await gameStore.fetchLevelEmails(props.levelId)
        
        if (!result.success) {
          ElMessage.error(result.message)
        }
      } catch (error) {
        console.error('加载关卡数据失败:', error)
        ElMessage.error('加载关卡数据失败，请稍后再试')
      } finally {
        loading.value = false
      }
    }
    
    // 监听levelId变化，重新加载数据
    watch(() => props.levelId, (newLevelId) => {
      if (newLevelId) {
        loadLevelData()
      }
    })
    
    // 组件挂载时加载数据
    onMounted(() => {
      loadLevelData()
    })
    
    // 标记为钓鱼邮件提示
    const identifyPhishingPrompt = () => {
      if (!selectedEmail.value) {
        ElMessage.warning('请先选择一封邮件');
        return;
      }
      
      ElMessageBox.confirm(
        '确定要将选中的邮件标记为钓鱼邮件吗？它将被移入垃圾桶。',
        '标记钓鱼邮件',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(() => {
        moveCurrentEmailToTrash();
      }).catch(() => {});
    };
    
    // 跳转回选关页面
    const goToLevels = () => {
      router.push('/game/levels')
    }
    
    return {
      loading,
      currentLevel,
      inboxEmails,
      trashEmails,
      selectedEmail,
      gameResult,
      isLastLevel,
      resultModalVisible,
      isDragOverTrash,
      isDragOverInbox,
      currentView,
      isSelectedEmailInTrash,
      isEmailRead,
      selectEmail,
      handleDragStart,
      getCurrentUserInitial,
      handleDragOverTrash,
      handleDragLeaveTrash,
      handleDropToTrash,
      handleDragOverInbox,
      handleDragLeaveInbox,
      handleDropToInbox,
      moveCurrentEmailToTrash,
      moveToTrash,
      restoreFromTrash,
      restoreCurrentEmail,
      switchView,
      submitLevel,
      goToNextLevel,
      viewSummary,
      exitGame,
      identifyPhishingPrompt,
      goToLevels
    }
  }
}
</script>

<style scoped>
.game-play-container {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f3f2f1;
  overflow: hidden;
}

/* Outlook 顶部导航栏 */
.outlook-header {
  display: flex;
  align-items: center;
  height: 48px;
  padding: 0 16px;
  background-color: #0078d4;
  color: white;
}

.outlook-logo {
  font-size: 18px;
  font-weight: bold;
  margin-right: 20px;
}

.outlook-search {
  flex: 1;
  max-width: 400px;
}

.outlook-search :deep(.el-input__inner) {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
}

.outlook-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
}

.header-icon {
  font-size: 20px;
  cursor: pointer;
  padding: 6px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.header-icon:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

/* Outlook 工具栏 */
.outlook-toolbar {
  background-color: white;
  border-bottom: 1px solid #e1dfdd;
  padding: 0 16px;
}

.toolbar-tabs {
  display: flex;
  height: 40px;
  border-bottom: 1px solid #e1dfdd;
}

.tab {
  padding: 0 16px;
  display: flex;
  align-items: center;
  font-size: 14px;
  cursor: pointer;
  position: relative;
  color: #616161;
}

.tab.active {
  color: #0078d4;
}

.tab.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background-color: #0078d4;
}

.toolbar-actions {
  display: flex;
  align-items: center;
  height: 56px;
  gap: 16px;
}

.action-group {
  display: flex;
  align-items: center;
  gap: 8px;
  padding-right: 16px;
  border-right: 1px solid #e1dfdd;
}

.game-action-group {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
}

/* 关卡信息提示 */
.level-info-banner {
  margin: 8px 16px;
}

/* 拖拽提示 */
.drag-hint-banner {
  margin: 8px 16px;
}

/* 邮箱客户端 */
.email-client {
  flex: 1;
  display: flex;
  overflow: hidden;
  margin: 0 16px 16px;
  background-color: white;
  box-shadow: 0 1.6px 3.6px 0 rgba(0,0,0,0.1);
}

/* 侧边栏 */
.sidebar {
  width: 240px;
  border-right: 1px solid #e1dfdd;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.user-profile {
  display: flex;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #e1dfdd;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #0078d4;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: bold;
  margin-right: 12px;
}

.user-info {
  flex: 1;
  overflow: hidden;
}

.username {
  font-weight: 600;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.email {
  font-size: 12px;
  color: #616161;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.folder-header {
  padding: 8px 16px;
  font-size: 12px;
  color: #616161;
  font-weight: 600;
  margin-top: 8px;
}

.folder {
  display: flex;
  align-items: center;
  padding: 8px 16px;
  cursor: pointer;
  color: #616161;
  transition: background-color 0.2s ease, transform 0.1s ease;
  position: relative;
}

.folder:hover {
  background-color: #f3f2f1;
  transform: translateY(-1px);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.folder.active {
  background-color: #c7e0f4;
  color: #0078d4;
  font-weight: 500;
}

.folder.drag-over {
  background-color: #c7e0f4;
  border: 2px dashed #0078d4;
  transform: scale(1.02);
}

.folder i {
  margin-right: 12px;
  font-size: 16px;
}

.folder .count {
  margin-left: auto;
  font-size: 12px;
  background-color: #0078d4;
  color: white;
  border-radius: 10px;
  min-width: 20px;
  height: 20px;
  line-height: 20px;
  text-align: center;
  padding: 0 6px;
}

/* 邮件内容区 */
.email-content-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.email-list-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  height: 40px;
  border-bottom: 1px solid #e1dfdd;
}

.list-title {
  font-weight: 600;
}

.list-actions {
  display: flex;
  gap: 16px;
}

.email-list {
  width: 360px;
  border-right: 1px solid #e1dfdd;
  overflow-y: auto;
  height: 100%;
}

.content-area {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}

/* 邮件列表动画效果 */
.email-list-container {
  position: relative;
}

.email-list-enter-active,
.email-list-leave-active {
  transition: all 0.3s ease;
}

.email-list-enter-from {
  opacity: 0;
  transform: translateX(-20px);
}

.email-list-leave-to {
  opacity: 0;
  transform: translateX(20px);
  position: absolute;
  width: 100%;
}

.email-list-move {
  transition: transform 0.5s ease;
}

/* 垃圾桶震动动画 */
@keyframes shake {
  0% { transform: translateX(0); }
  20% { transform: translateX(-5px); }
  40% { transform: translateX(5px); }
  60% { transform: translateX(-3px); }
  80% { transform: translateX(3px); }
  100% { transform: translateX(0); }
}

.shake-animation {
  animation: shake 0.5s ease-in-out;
}

/* 邮件内容工具栏 */
.content-toolbar {
  display: flex;
  justify-content: flex-start;
  padding: 8px 16px;
  background-color: #f9f8f7;
  border-bottom: 1px solid #edebe9;
}

.toolbar-actions {
  display: flex;
  gap: 8px;
}

.toolbar-button {
  width: 32px;
  height: 32px;
  border-radius: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #605e5c;
  transition: all 0.2s ease;
}

.toolbar-button:hover {
  background-color: #edebe9;
  color: #323130;
}

.action-icon {
  cursor: pointer;
  padding: 4px;
  border-radius: 2px;
  transition: all 0.2s ease;
}

.action-icon:hover {
  background-color: #edebe9;
}

/* 高亮按钮样式 */
.highlight-button {
  background-color: #0078d4;
  color: white;
}

.highlight-button:hover {
  background-color: #106ebe;
  color: white;
}

/* 垃圾桶脉冲动画 */
@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.pulse-animation {
  animation: pulse 0.5s infinite;
  background-color: rgba(0, 120, 212, 0.1);
}

/* 收件箱拖拽接收区域 */
.folder.drag-over.active {
  background-color: #c7e0f4;
  border: 2px dashed #0078d4;
  transform: scale(1.02);
}

/* 用户头像 */
.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: #0078d4;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: bold;
  margin-left: 16px;
}
</style> 