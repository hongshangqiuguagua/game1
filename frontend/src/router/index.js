import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// 路由配置
const routes = [
  {
    path: '/',
    name: 'Start',
    component: () => import('@/views/Start.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/game',
    component: () => import('@/views/GameLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/game/levels'
      },
      {
        path: 'levels',
        name: 'LevelSelect',
        component: () => import('@/views/LevelSelect.vue')
      },
      {
        path: 'play/:levelId',
        name: 'GamePlay',
        component: () => import('@/views/GamePlay.vue'),
        props: true
      }
    ]
  },
  {
    path: '/summary',
    name: 'Summary',
    component: () => import('@/views/Summary.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('@/views/AdminLayout.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: '',
        redirect: '/admin/levels'
      },
      {
        path: 'levels',
        name: 'AdminLevels',
        component: () => import('@/views/admin/LevelManagement.vue')
      },
      {
        path: 'emails/:levelId',
        name: 'AdminEmails',
        component: () => import('@/views/admin/EmailManagement.vue'),
        props: true
      },
      {
        path: 'statistics',
        name: 'AdminStatistics',
        component: () => import('@/views/admin/Statistics.vue')
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue')
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// 全局前置守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const isLoggedIn = authStore.isLoggedIn
  const isAdmin = authStore.isAdmin
  
  // 需要登录的页面
  if (to.meta.requiresAuth && !isLoggedIn) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
    return
  }
  
  // 需要管理员权限的页面
  if (to.meta.requiresAdmin && !isAdmin) {
    next({ name: 'Start' })
    return
  }
  
  // 已登录用户访问登录或注册页面时重定向到游戏页面
  if (isLoggedIn && (to.name === 'Login' || to.name === 'Register')) {
    next({ name: 'LevelSelect' })
    return
  }
  
  next()
})

export default router 