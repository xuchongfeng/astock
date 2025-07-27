import axios from 'axios';
import API_CONFIG from './config';

const api = axios.create({
  baseURL: API_CONFIG.baseURL,
  timeout: API_CONFIG.timeout,
});

export const strategyApi = {
  // 策略表
  getStrategies: (params = {}) => api.get('/api/strategy', { params }),
  getStrategy: (id) => api.get(`/api/strategy/${id}`),
  addStrategy: (data) => api.post('/api/strategy', data),
  updateStrategy: (id, data) => api.put(`/api/strategy/${id}`, data),
  deleteStrategy: (id) => api.delete(`/api/strategy/${id}`),

  // 策略关联股票表
  getStrategyStocks: (params = {}) => api.get('/api/strategy_stock', { params }),
  addStrategyStock: (data) => api.post('/api/strategy_stock', data),
  deleteStrategyStock: (id) => api.delete(`/api/strategy_stock/${id}`),
}; 