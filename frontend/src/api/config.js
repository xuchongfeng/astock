// API基础配置
const API_CONFIG = {
  baseURL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000/api',
  timeout: 60000, // 调整为1分钟
};

export const ENDPOINTS = {
  COMPANY: '/api/stock_company',
  DAILY: '/api/stock_daily',
  INDUSTRY: '/api/industry',
  INDUSTRY_STATS: '/api/industry_stats',
};

export default API_CONFIG;