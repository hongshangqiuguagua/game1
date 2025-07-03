/**
 * 应用配置
 * 在实际部署时，可以根据环境修改这些值
 */

// API基础URL
export const API_BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000';

// 应用标题
export const APP_TITLE = process.env.VUE_APP_TITLE || '钓鱼邮件识别教学游戏';

// 调试模式
export const DEBUG = process.env.VUE_APP_DEBUG === 'true';

// 默认分页大小
export const DEFAULT_PAGE_SIZE = 10;

// 令牌存储键名
export const TOKEN_KEY = 'token';
export const USER_KEY = 'user';

// 其他配置
export default {
  API_BASE_URL,
  APP_TITLE,
  DEBUG,
  DEFAULT_PAGE_SIZE,
  TOKEN_KEY,
  USER_KEY
}; 