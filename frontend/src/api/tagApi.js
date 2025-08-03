import axios from 'axios';
import API_CONFIG from './config';

const api = axios.create({
  baseURL: API_CONFIG.baseURL,
  timeout: API_CONFIG.timeout,
});

export const tagApi = {
  // 获取所有标签
  getTags: (params = {}) => api.get('/api/tags', { params }),
  
  // 获取单个标签
  getTag: (id) => api.get(`/api/tags/${id}`),
  
  // 创建标签
  createTag: (data) => api.post('/api/tags', data),
  
  // 更新标签
  updateTag: (id, data) => api.put(`/api/tags/${id}`, data),
  
  // 删除标签
  deleteTag: (id) => api.delete(`/api/tags/${id}`),
  
  // 获取股票的所有标签
  getStockTags: (tsCode, params = {}) => api.get(`/api/stocks/${tsCode}/tags`, { params }),
  
  // 为股票添加标签
  addStockTag: (tsCode, data) => api.post(`/api/stocks/${tsCode}/tags`, data),
  
  // 更新股票标签
  updateStockTag: (tsCode, tagId, data) => api.put(`/api/stocks/${tsCode}/tags/${tagId}`, data),
  
  // 删除股票标签
  deleteStockTag: (tsCode, tagId) => api.delete(`/api/stocks/${tsCode}/tags/${tagId}`),
  
  // 获取用户的所有股票标签
  getUserStockTags: (userId, params = {}) => api.get(`/api/users/${userId}/stock-tags`, { params }),
}; 