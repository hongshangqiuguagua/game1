<template>
  <div
    class="trash-bin"
    :class="{ 'drag-over': isDragOver }"
    @dragover="handleDragOver"
    @dragleave="handleDragLeave"
    @drop="handleDrop"
  >
    <div class="trash-icon">
      <el-icon><el-icon-delete></el-icon-delete></el-icon>
    </div>
    <div class="trash-text">垃圾桶</div>
    <div class="trash-count" v-if="count > 0">{{ count }}</div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'TrashBin',
  
  props: {
    count: {
      type: Number,
      default: 0
    }
  },
  
  emits: ['drop'],
  
  setup(props, { emit }) {
    const isDragOver = ref(false)
    
    // 拖拽经过垃圾桶
    const handleDragOver = (event) => {
      event.preventDefault()
      event.dataTransfer.dropEffect = 'move'
      isDragOver.value = true
    }
    
    // 拖拽离开垃圾桶
    const handleDragLeave = () => {
      isDragOver.value = false
    }
    
    // 拖拽放置到垃圾桶
    const handleDrop = (event) => {
      event.preventDefault()
      isDragOver.value = false
      
      // 获取拖拽的邮件ID
      const emailId = event.dataTransfer.getData('text/plain')
      if (emailId) {
        emit('drop', parseInt(emailId))
        
        // 播放动画效果
        const trashBin = event.currentTarget
        trashBin.classList.add('drop-animation')
        setTimeout(() => {
          trashBin.classList.remove('drop-animation')
        }, 300)
      }
    }
    
    return {
      isDragOver,
      handleDragOver,
      handleDragLeave,
      handleDrop
    }
  }
}
</script>

<style scoped>
.trash-bin {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 15px;
  border: 2px dashed #dcdfe6;
  border-radius: 4px;
  background-color: #f5f7fa;
  transition: all 0.3s;
  position: relative;
  cursor: pointer;
  height: 100%;
  min-height: 100px;
}

.trash-bin:hover {
  background-color: #ecf5ff;
  border-color: #c6e2ff;
}

.trash-bin.drag-over {
  background-color: #ecf5ff;
  border-color: #409eff;
  transform: scale(1.05);
}

.trash-icon {
  font-size: 24px;
  color: #909399;
  margin-bottom: 5px;
}

.trash-bin.drag-over .trash-icon {
  color: #409eff;
}

.trash-text {
  font-size: 14px;
  color: #606266;
}

.trash-bin.drag-over .trash-text {
  color: #409eff;
}

.trash-count {
  position: absolute;
  top: 5px;
  right: 5px;
  background-color: #f56c6c;
  color: #fff;
  border-radius: 10px;
  min-width: 20px;
  height: 20px;
  line-height: 20px;
  text-align: center;
  font-size: 12px;
  padding: 0 6px;
}

/* 放置动画 */
@keyframes dropAnimation {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

.drop-animation {
  animation: dropAnimation 0.3s ease;
}
</style> 