import axios from 'axios';
import API_CONFIG from './config';

const api = axios.create({
  baseURL: API_CONFIG.baseURL,
  timeout: API_CONFIG.timeout,
});

export const deepseekApi = {
  // 获取股票基础信息分析
  getStockBasicAnalysis: (tsCode) => api.get(`/api/deepseek_analysis/stock/basic_info/${tsCode}`),
  
  // 获取股票走势分析
  getStockDailyAnalysis: (tsCode) => api.get(`/api/deepseek_analysis/stock/daily/${tsCode}`),
  
  // 获取股票技术分析
  getStockTechnicalAnalysis: (tsCode) => api.get(`/api/deepseek_analysis/stock/technical/${tsCode}`),
  
  // 获取股票基本面分析
  getStockFundamentalAnalysis: (tsCode) => api.get(`/api/deepseek_analysis/stock/fundamental/${tsCode}`),
  
  // 获取股票风险评估
  getStockRiskAnalysis: (tsCode) => api.get(`/api/deepseek_analysis/stock/risk/${tsCode}`),
  
  // 获取股票投资建议
  getStockInvestmentAdvice: (tsCode) => api.get(`/api/deepseek_analysis/stock/advice/${tsCode}`),
}; 