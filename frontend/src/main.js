import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/es/locale/lang/zh-cn'

// 导入Element Plus图标
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

// 创建Vue应用
const app = createApp(App)

// 注册所有Element Plus图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(`ElIcon${key}`, component)
}

// 使用Pinia状态管理
const pinia = createPinia()
app.use(pinia)

// 使用Vue Router
app.use(router)

// 使用Element Plus并设置为中文
app.use(ElementPlus, {
  locale: zhCn
})

// 挂载应用
app.mount('#app') 