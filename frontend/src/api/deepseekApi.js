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
  
  // 获取市场概况分析
  getMarketOverview: (date) => api.get('/api/deepseek_analysis/market/overview', { params: { date } }),
  
  // 获取综合分析市场
  getMarketComprehensive: () => api.get('/api/deepseek_analysis/market/comprehensive'),
  
  // 获取行业分析
  getIndustryAnalysis: (industryName, date) => api.get(`/api/deepseek_analysis/industry/${industryName}`, { params: { date } }),
}; 