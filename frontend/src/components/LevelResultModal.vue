<template>
  <el-dialog
    :model-value="visible"
    @update:model-value="emit('update:visible', $event)"
    :title="isLastLevel ? '挑战完成！' : '本关结束'"
    width="50%"
    :close-on-click-modal="false"
    @closed="close"
  >
    <div>
      <el-result
        :icon="result.correct_count === result.total_count ? 'success' : 'warning'"
        :title="`答对 ${result.correct_count} / ${result.total_count}`"
      >
        <template #sub-title>
          <p>正确率: {{ ((result.correct_count / result.total_count) * 100).toFixed(0) }}%</p>
        </template>
      </el-result>

      <div v-if="result.trick_summary" class="trick-summary">
        <h4>本关骗术总结</h4>
        <p>{{ result.trick_summary }}</p>
      </div>

      <div class="results-list">
        <h4>详细结果</h4>
        <el-scrollbar height="200px">
          <ul>
            <li v-for="item in result.results" :key="item.email_id">
              <el-icon :color="item.correct ? '#67C23A' : '#F56C6C'">
                <component :is="item.correct ? 'Check' : 'Close'" />
              </el-icon>
              <span v-if="item.subject">{{ item.subject }}:</span>
              <span v-else>邮件ID {{ item.email_id }}:</span>
              <span v-if="item.correct">判断正确。</span>
              <span v-else>
                判断错误。
                <span v-if="item.is_phishing">这其实是一封钓鱼邮件。</span>
                <span v-else>这其实是一封正常邮件。</span>
              </span>
              <p v-if="!item.correct && item.phishing_clue" class="clue">
                提示: {{ item.phishing_clue }}
              </p>
            </li>
          </ul>
        </el-scrollbar>
      </div>
    </div>
    <template #footer>
      <el-button @click="close">返回选关</el-button>
      <el-button v-if="!isLastLevel" type="primary" @click="next">
        下一关
      </el-button>
      <el-button v-else type="success" @click="viewSummary">
        查看游戏总结
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { computed } from 'vue';
import { Check, Close } from '@element-plus/icons-vue';

const props = defineProps({
  visible: {
    type: Boolean,
    required: true
  },
  result: {
    type: Object,
    required: true
  },
  isLastLevel: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:visible', 'nextLevel', 'viewSummary', 'goToLevels', 'closed']);

// 当用户点击关闭按钮
const close = () => {
  emit('update:visible', false);
  emit('goToLevels'); // 添加这个事件，通知父组件跳转到选关页面
};

// 进入下一关
const next = () => {
  emit('nextLevel');
};

// 查看总结
const viewSummary = () => {
  emit('viewSummary');
};
</script>

<style scoped>
.trick-summary {
  background-color: #f4f4f5;
  padding: 10px 20px;
  border-radius: 4px;
  margin: 20px 0;
}
.results-list ul {
  list-style-type: none;
  padding-left: 0;
}
.results-list li {
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}
.results-list .el-icon {
  margin-right: 8px;
  font-size: 1.2em;
}
.clue {
  font-size: 0.9em;
  color: #909399;
  margin-left: 20px;
  width: 100%;
}
</style> 