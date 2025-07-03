<template>
  <div
    class="email-item"
    :class="{ 
      'read': isRead, 
      'unread': !isRead, 
      'selected': isSelected,
      'in-trash': isInTrash
    }"
    @click="handleClick"
    draggable="true"
    @dragstart="handleDragStart"
    @dragend="handleDragEnd"
    @mouseover="showDragHint = true"
    @mouseleave="showDragHint = false"
  >
    <div class="drag-indicator" :class="{'visible': showDragHint}">
      <div class="drag-dots"></div>
    </div>
    <div class="email-sender">
      <div class="sender-avatar">{{ getSenderInitial() }}</div>
      <div class="sender-info">
        <div class="sender-name">{{ email.from_name }}</div>
        <div class="email-subject">{{ email.subject }}</div>
      </div>
    </div>
    <div class="email-preview">
      <div class="preview-text">{{ getPreviewText() }}</div>
      <div class="email-date">{{ getFormattedDate() }}</div>
      
      <!-- 恢复按钮（仅在垃圾箱中显示） -->
      <div v-if="isInTrash" class="email-restore-btn" @click.stop="handleRestore">
        <el-tooltip content="恢复至收件箱" placement="left">
          <el-icon><el-icon-top-right /></el-icon>
        </el-tooltip>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  name: 'EmailItem',
  
  props: {
    email: {
      type: Object,
      required: true
    },
    isRead: {
      type: Boolean,
      default: false
    },
    isSelected: {
      type: Boolean,
      default: false
    },
    isInTrash: {
      type: Boolean,
      default: false
    }
  },
  
  emits: ['click', 'dragstart', 'restore'],
  
  setup(props, { emit }) {
    const isDragging = ref(false);
    const showDragHint = ref(false);
    
    // 获取邮件预览文本
    const getPreviewText = () => {
      if (!props.email.content) return '';
      // 移除HTML标签并截取前50个字符
      const plainText = props.email.content.replace(/<[^>]*>/g, '');
      return plainText.length > 50 ? plainText.substring(0, 50) + '...' : plainText;
    };
    
    // 获取格式化日期
    const getFormattedDate = () => {
      // 在实际应用中，这里会使用邮件的收到日期
      // 这里我们只是模拟随机的日期字符串
      const dates = ['今天', '昨天', '周一', '周二', '6月12日', '6月10日'];
      const randomIndex = Math.floor(Math.random() * dates.length);
      return dates[randomIndex];
    };
    
    // 获取发件人首字母
    const getSenderInitial = () => {
      if (props.email && props.email.from_name) {
        return props.email.from_name.charAt(0).toUpperCase();
      }
      return '?';
    };
    
    // 点击邮件
    const handleClick = () => {
      // 添加点击效果
      const element = event.currentTarget;
      element.classList.add('click-effect');
      setTimeout(() => {
        element.classList.remove('click-effect');
      }, 200);
      
      emit('click', props.email.id);
    };
    
    // 开始拖拽邮件
    const handleDragStart = (event) => {
      isDragging.value = true;
      
      // 设置拖拽数据
      event.dataTransfer.setData('text/plain', props.email.id);
      event.dataTransfer.effectAllowed = 'move';
      
      // 通知父组件
      emit('dragstart', event, props.email.id);
    };
    
    // 拖拽结束
    const handleDragEnd = () => {
      isDragging.value = false;
    };
    
    // 恢复邮件（从垃圾箱）
    const handleRestore = () => {
      emit('restore', props.email.id);
    };
    
    return {
      isDragging,
      showDragHint,
      getPreviewText,
      getFormattedDate,
      getSenderInitial,
      handleClick,
      handleDragStart,
      handleDragEnd,
      handleRestore
    };
  }
};
</script>

<style scoped>
.email-item {
  padding: 12px 16px 12px 32px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: all 0.2s ease;
  background-color: #ffffff;
  position: relative;
}

.email-item:hover {
  background-color: #f3f2f1;
  z-index: 1;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transform: translateY(-1px);
}

.email-item.selected {
  background-color: #c7e0f4;
}

.email-item.unread {
  font-weight: 600;
  background-color: #f0f8ff;
}

.email-item.in-trash {
  opacity: 0.85;
  background-color: #f9f9f9;
  border-left: 3px solid #e57373;
}

/* 拖动指示器 */
.drag-indicator {
  position: absolute;
  left: 8px;
  top: 50%;
  transform: translateY(-50%);
  width: 12px;
  height: 20px;
  opacity: 0;
  transition: opacity 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.drag-indicator.visible {
  opacity: 0.7;
}

.drag-dots {
  width: 4px;
  height: 12px;
  background-image: radial-gradient(circle, #888 1.5px, transparent 1.5px);
  background-size: 4px 4px;
  background-repeat: repeat-y;
}

.email-item:hover .drag-indicator {
  opacity: 0.7;
}

.email-item:active .drag-indicator {
  opacity: 1;
}

.email-sender {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.sender-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background-color: #5c6bc0;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
  margin-right: 10px;
}

.email-item.in-trash .sender-avatar {
  background-color: #9e9e9e;
}

.sender-info {
  flex: 1;
  overflow: hidden;
}

.sender-name {
  font-weight: 500;
  margin-bottom: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.email-subject {
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.email-preview {
  display: flex;
  align-items: flex-start;
  flex-direction: column;
  font-size: 13px;
  color: #666;
  position: relative;
}

.preview-text {
  max-height: 40px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  margin-bottom: 4px;
}

.email-date {
  font-size: 12px;
  color: #888;
  align-self: flex-end;
}

/* 点击效果 */
@keyframes clickEffect {
  0% { transform: scale(1); }
  50% { transform: scale(0.98); }
  100% { transform: scale(1); }
}

.click-effect {
  animation: clickEffect 0.2s ease;
}

/* 恢复按钮 */
.email-restore-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background-color: rgba(0, 120, 212, 0.1);
  opacity: 0;
  transition: all 0.2s ease;
  color: #0078d4;
}

.email-item:hover .email-restore-btn {
  opacity: 1;
  background-color: rgba(0, 120, 212, 0.15);
}

.email-restore-btn:hover {
  background-color: #0078d4;
  color: white;
  transform: scale(1.1);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 拖拽时的样式 */
.email-item:active {
  cursor: grabbing;
  transform: scale(0.98);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  opacity: 0.9;
}
</style> 