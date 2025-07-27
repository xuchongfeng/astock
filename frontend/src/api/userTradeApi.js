import axios from 'axios';
import API_CONFIG from './config';

const api = axios.create({
  baseURL: API_CONFIG.baseURL,
  timeout: API_CONFIG.timeout,
});

export const userTradeApi = {
  // 获取用户交易记录列表
  getTrades: (userId, params = {}) => api.get(`/api/user_trade/${userId}`, { params }),
  // 获取单条交易记录
  getTrade: (userId, id) => api.get(`/api/user_trade/${userId}/detail/${id}`),
  // 新增交易记录
  addTrade: (userId, data) => api.post(`/api/user_trade/${userId}`, data),
  // 更新交易记录
  updateTrade: (userId, id, data) => api.put(`/api/user_trade/${userId}/${id}`, data),
  // 删除交易记录
  deleteTrade: (userId, id) => api.delete(`/api/user_trade/${userId}/${id}`),
}; 