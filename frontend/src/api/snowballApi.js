import axios from 'axios';
import API_CONFIG from './config';

const api = axios.create({
  baseURL: API_CONFIG.baseURL,
  timeout: API_CONFIG.timeout,
});

export const snowballApi = {
  // 股票分组相关API
  getGroups: (params = {}) => api.get(`/api/xueqiu/portfolio/groups`, { params }),
  getGroup: (groupId) => api.get(`/api/xueqiu/portfolio/groups/${groupId}`),
  createGroup: (data) => api.post(`/api/xueqiu/portfolio/groups`, data),
  updateGroup: (groupId, data) => api.put(`/api/xueqiu/portfolio/groups/${groupId}`, data),
  deleteGroup: (groupId) => api.delete(`/api/xueqiu/portfolio/groups/${groupId}`),

  // 分组内股票相关API
  getGroupStocks: (groupId, params = {}) => api.get(`/api/xueqiu/portfolio/groups/${groupId}/stocks`, { params }),
  addStockToGroup: (groupId, data) => api.post(`/api/xueqiu/portfolio/groups/${groupId}/stocks`, data),
  removeStockFromGroup: (groupId, stockId) => api.delete(`/api/xueqiu/portfolio/groups/${groupId}/stocks/${stockId}`),
  updateStockInGroup: (groupId, stockId, data) => api.put(`/api/xueqiu/portfolio/groups/${groupId}/stocks/${stockId}`, data),
}; 