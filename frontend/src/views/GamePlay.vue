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
          <el-button type="primary" size="small" disabled class="disabled-button">
            <el-icon><el-icon-plus /></el-icon>
            <span>新邮件</span>
          </el-button>
        </div>
        <div class="action-group">
          <el-button type="text" size="small" disabled class="disabled-button">
            <el-icon><el-icon-delete /></el-icon>
            <span>删除</span>
          </el-button>
          <el-button type="text" size="small" disabled class="disabled-button">
            <el-icon><el-icon-folder /></el-icon>
            <span>存档</span>
          </el-button>
          <el-button v-if="currentView === 'inbox'" type="warning" size="small" @click="identifyPhishingPrompt" class="operable-button">
            <el-icon><el-icon-warning /></el-icon>
            <span>标记为钓鱼邮件</span>
            <div class="action-hint">点击标记</div>
          </el-button>
          <el-button v-else type="success" size="small" @click="switchView('inbox')" class="operable-button">
            <el-icon><el-icon-back /></el-icon>
            <span>返回收件箱</span>
            <div class="action-hint">点击返回</div>
          </el-button>
        </div>
        
        <!-- 游戏操作按钮组 -->
        <div class="game-action-group">
          <el-button type="warning" @click="exitGame" :disabled="loading" class="operable-button">
            退出游戏
            <div class="action-hint">点击退出</div>
          </el-button>
          <el-button type="primary" @click="submitLevel" :disabled="loading" class="operable-button">
            完成本关
            <div class="action-hint">完成判断</div>
          </el-button>
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
    
    <!-- 拖拽教程动画 -->
    <div v-if="showTutorial" class="tutorial-overlay" @click="dismissTutorial">
      <div class="tutorial-content" @click.stop>
        <div class="tutorial-header">
          <div class="tutorial-title">邮件拖拽功能</div>
          <el-button type="text" @click="dismissTutorial" class="tutorial-close">
            <el-icon><el-icon-close /></el-icon>
          </el-button>
        </div>
        <div class="tutorial-body">
          <div class="tutorial-step">
            <div class="tutorial-animation">
              <div class="animation-email"></div>
              <div class="animation-arrow"></div>
              <div class="animation-folder"></div>
            </div>
            <div class="tutorial-text">
              <p>在本游戏中，您可以通过拖拽方式将可疑邮件移至垃圾桶，或将误删的邮件恢复到收件箱。</p>
              <p>请尝试点击并拖动邮件至对应的文件夹。</p>
            </div>
          </div>
        </div>
        <div class="tutorial-footer">
          <el-checkbox v-model="dontShowAgain">不再显示</el-checkbox>
          <el-button type="primary" @click="dismissTutorial">我知道了</el-button>
        </div>
      </div>
    </div>
    
    <div class="email-client" v-if="!loading">
      <div class="sidebar">
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
          :class="{ active: currentView === 'inbox', 'drag-over': isDragOverInbox, 'operable-folder': true }"
            data-folder="inbox"
            @click="switchView('inbox')"
            @dragover="handleDragOverInbox"
            @dragleave="handleDragLeaveInbox"
            @drop="handleDropToInbox"
          >
            <el-icon><el-icon-message /></el-icon>
            <span>收件箱</span>
            <span class="count" v-if="inboxEmails.length > 0">{{ inboxEmails.length }}</span>
          <div class="folder-hint" v-if="currentView !== 'inbox'">可拖放区域</div>
          </div>
        <div class="folder non-interactive">
            <el-icon><el-icon-star /></el-icon>
            <span>已加星标</span>
          </div>
          
          <div class="folder-header">文件夹</div>
          <div 
            class="folder" 
          :class="{ active: currentView === 'trash', 'drag-over': isDragOverTrash, 'operable-folder': true }" 
            data-folder="trash" 
            @click="switchView('trash')"
            @dragover="handleDragOverTrash" 
            @dragleave="handleDragLeaveTrash" 
            @drop="handleDropToTrash"
          >
            <el-icon><el-icon-delete /></el-icon>
            <span>垃圾桶</span>
            <span class="count" v-if="trashEmails.length > 0">{{ trashEmails.length }}</span>
          <div class="folder-hint" v-if="currentView !== 'trash'">可拖放区域</div>
          </div>
        <div class="folder non-interactive">
            <el-icon><el-icon-position /></el-icon>
            <span>已发送</span>
          </div>
        <div class="folder non-interactive">
            <el-icon><el-icon-document /></el-icon>
            <span>草稿</span>
          </div>
        <div class="folder non-interactive">
            <el-icon><el-icon-folder /></el-icon>
            <span>存档</span>
        </div>
      </div>
      
      <div class="email-content-wrapper">
        <div class="email-container">
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
      </div>
      
      <div class="content-area">
          <div v-if="selectedEmail" class="content-toolbar">
            <div class="toolbar-actions">
              <el-tooltip content="回复" placement="bottom">
                <div class="toolbar-button disabled-button"><el-icon><el-icon-reply /></el-icon></div>
              </el-tooltip>
              <el-tooltip content="转发" placement="bottom">
                <div class="toolbar-button disabled-button"><el-icon><el-icon-share /></el-icon></div>
              </el-tooltip>
              
              <!-- 根据当前视图显示不同的操作按钮 -->
              <template v-if="isSelectedEmailInTrash">
                <el-tooltip content="恢复邮件" placement="bottom">
                  <div class="toolbar-button highlight-button operable-button" @click="restoreCurrentEmail">
                    <el-icon><el-icon-top /></el-icon>
                    <div class="button-action-hint">点击恢复</div>
                  </div>
                </el-tooltip>
              </template>
              <template v-else>
                <el-tooltip content="移至垃圾桶" placement="bottom">
                  <div class="toolbar-button operable-button" @click="moveCurrentEmailToTrash">
                    <el-icon><el-icon-delete /></el-icon>
                    <div class="button-action-hint">点击删除</div>
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
    
    // 教程相关
    const tutorialKey = 'phishing_game_tutorial_shown'
    const showTutorial = ref(false)
    const dontShowAgain = ref(false)
    
    // 检查是否应显示教程
    onMounted(() => {
      try {
        const tutorialShown = localStorage.getItem(tutorialKey)
        if (!tutorialShown) {
          showTutorial.value = true
        }
      } catch (e) {
        console.error('无法访问本地存储:', e)
        showTutorial.value = true
      }
    })
    
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
    
    // 关闭教程
    const dismissTutorial = () => {
      showTutorial.value = false;
      
      // 保存用户不再显示的选择
      if (dontShowAgain.value) {
        try {
          localStorage.setItem(tutorialKey, 'true');
        } catch (e) {
          console.error('无法保存到本地存储:', e);
        }
      }
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
      goToLevels,
      showTutorial,
      dontShowAgain,
      dismissTutorial
    }
  }
}
</script>

<style scoped>
.game-play-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
  position: relative;
  background-color: transparent;
  z-index: 1;
}

/* Outlook 顶部导航栏 */
.outlook-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 48px;
  padding: 0 16px;
  background-color: rgba(0, 120, 212, 0.85);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  color: white;
  z-index: 2;
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
  background-color: rgba(255, 255, 255, 0.95);
  border-bottom: 1px solid #e1dfdd;
  padding: 0 16px;
  z-index: 2;
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
  display: flex;
  flex: 1;
  overflow: hidden;
}

.sidebar {
  width: 250px;
  background-color: rgba(255, 255, 255, 0.9);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  border-right: 1px solid rgba(225, 223, 221, 0.6);
}

.user-profile {
  display: flex;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid rgba(225, 223, 221, 0.6);
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
  padding: 12px 20px;
  cursor: pointer;
  color: #616161;
  transition: all 0.3s ease;
  position: relative;
  border: 2px solid transparent;
  overflow: hidden;
  height: 48px;
  margin-bottom: 2px;
}

.folder:hover {
  background-color: rgba(243, 242, 241, 0.7);
  transform: translateY(-1px);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.folder[data-folder="inbox"],
.folder[data-folder="trash"] {
  border-left: 3px solid transparent;
  transition: all 0.3s ease;
  animation: subtle-highlight 3s infinite alternate;
}

.folder[data-folder="inbox"] {
  border-left-color: #0078d4;
}

.folder[data-folder="trash"] {
  border-left-color: #d13438;
}

@keyframes subtle-highlight {
  0% { border-left-width: 3px; }
  100% { border-left-width: 5px; }
}

.folder.active {
  background-color: rgba(199, 224, 244, 0.8);
  color: #0078d4;
  font-weight: 500;
}

.folder.drag-over {
  background-color: rgba(0, 120, 212, 0.15);
  border: 2px dashed #0078d4;
  transform: scale(1.02);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  animation: folderPulse 1.5s infinite;
}

@keyframes folderPulse {
  0% {
    background-color: rgba(0, 120, 212, 0.05);
  }
  50% {
    background-color: rgba(0, 120, 212, 0.2);
  }
  100% {
    background-color: rgba(0, 120, 212, 0.05);
  }
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
  flex-direction: row;
  overflow: hidden;
  background-color: rgba(255, 255, 255, 0.9);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin: 0 16px 16px;
}

.email-container {
  width: 360px;
  border-right: 1px solid #e1dfdd;
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
  overflow-y: auto;
  height: 100%;
}

.content-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  background-color: #fff;
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
  width: 100%;
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

/* 教程遮罩层 */
.tutorial-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.tutorial-content {
  background-color: white;
  padding: 24px;
  border-radius: 8px;
  max-width: 500px;
  max-height: 90%;
  overflow: auto;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  animation: tutorialFadeIn 0.5s ease;
  z-index: 1000;
}

@keyframes tutorialFadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.tutorial-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.tutorial-title {
  font-weight: 600;
}

.tutorial-close {
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
}

.tutorial-body {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tutorial-step {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.tutorial-animation {
  position: relative;
  width: 240px;
  height: 120px;
  margin-bottom: 16px;
  background-color: #f9f9f9;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.1);
}

.animation-email {
  position: absolute;
  width: 60px;
  height: 40px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  left: 30px;
  top: 40px;
  animation: dragEmail 4s infinite;
  z-index: 2;
}

.animation-email:before {
  content: "";
  position: absolute;
  left: 10px;
  top: 10px;
  width: 40px;
  height: 3px;
  background-color: #0078d4;
  border-radius: 2px;
  box-shadow: 0 8px 0 #0078d4, 0 16px 0 #0078d4;
  opacity: 0.7;
}

.animation-folder {
  position: absolute;
  width: 50px;
  height: 40px;
  background-color: rgba(0, 120, 212, 0.1);
  border: 2px dashed #0078d4;
  border-radius: 4px;
  right: 30px;
  top: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  animation: pulseFolder 2s infinite;
}

.animation-folder:before {
  content: "";
  position: absolute;
  width: 20px;
  height: 20px;
  background-color: transparent;
  border-radius: 2px;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%230078d4"><path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/></svg>');
  background-repeat: no-repeat;
  background-position: center;
  background-size: contain;
  opacity: 0.8;
}

.animation-arrow {
  position: absolute;
  width: 80px;
  height: 3px;
  background-color: #0078d4;
  top: 60px;
  left: 50%;
  transform: translateX(-50%);
  opacity: 0;
  animation: showArrow 4s infinite;
}

.animation-arrow:after {
  content: "";
  position: absolute;
  right: -3px;
  top: -5px;
  width: 0;
  height: 0;
  border-left: 8px solid #0078d4;
  border-top: 6px solid transparent;
  border-bottom: 6px solid transparent;
}

@keyframes dragEmail {
  0%, 15% {
    transform: translateX(0) scale(1);
  }
  20%, 45% {
    transform: translateX(120px) scale(0.9);
  }
  50%, 75% {
    transform: translateX(0) scale(1);
  }
  80%, 95% {
    transform: translateX(120px) scale(0.9);
  }
  100% {
    transform: translateX(0) scale(1);
  }
}

@keyframes pulseFolder {
  0%, 100% {
    background-color: rgba(0, 120, 212, 0.1);
    transform: scale(1);
  }
  50% {
    background-color: rgba(0, 120, 212, 0.2);
    transform: scale(1.05);
  }
}

@keyframes showArrow {
  0%, 15% {
    opacity: 0;
  }
  20%, 45% {
    opacity: 1;
  }
  50%, 75% {
    opacity: 0;
  }
  80%, 95% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}

.tutorial-text {
  text-align: center;
}

.tutorial-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
}

.tutorial-close {
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
}

/* 新增样式 */
.disabled-button {
  opacity: 0.6;
  cursor: not-allowed !important;
  color: #909399 !important;
  background-color: #f5f7fa !important;
  border-color: #e4e7ed !important;
}

.operable-button {
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.operable-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.operable-button:active {
  transform: translateY(0);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.operable-button::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: rgba(255, 255, 255, 0.5);
  transform: translateX(-100%);
  transition: transform 0.3s ease;
}

.operable-button:hover::after {
  transform: translateX(0);
}

.action-hint {
  position: absolute;
  bottom: -20px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 12px;
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 2px 6px;
  border-radius: 3px;
  white-space: nowrap;
  opacity: 0;
  transition: all 0.3s ease;
  pointer-events: none;
  z-index: 10;
}

.operable-button:hover .action-hint {
  opacity: 1;
  bottom: -25px;
}

.folder-hint {
  position: absolute;
  bottom: 0;
  right: 0;
  padding: 2px 4px;
  background-color: rgba(0, 120, 212, 0.1);
  color: #0078d4;
  border-radius: 2px 0 0 0;
  font-size: 10px;
  opacity: 0;
  transform: translateY(100%);
  transition: all 0.3s ease;
}

.operable-folder:hover .folder-hint {
  opacity: 1;
  transform: translateY(0);
}

.button-action-hint {
  position: absolute;
  top: -25px;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 10px;
  white-space: nowrap;
  opacity: 0;
  transition: all 0.3s ease;
  pointer-events: none;
}

.operable-button:hover .button-action-hint {
  opacity: 1;
  top: -20px;
}

.non-interactive {
  opacity: 0.6;
  cursor: default !important;
  color: #909399;
  background-color: #f5f7fa;
}

/* 添加高亮呼吸效果 */
.operable-folder {
  position: relative;
}

.operable-folder::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 120, 212, 0.05);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.operable-folder:hover::before {
  opacity: 1;
  animation: breatheEffect 2s infinite;
}

@keyframes breatheEffect {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 0.7; }
}

.email-button.disabled {
  pointer-events: none;
  opacity: 0.7;
}
</style> 