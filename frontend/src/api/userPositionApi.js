import axios from 'axios';
import API_CONFIG from './config';

const api = axios.create({
  baseURL: API_CONFIG.baseURL,
  timeout: API_CONFIG.timeout,
});

export const userPositionApi = {
  // 获取用户持仓列表
  getPositions: (userId, params = {}) => api.get(`/api/user_position/${userId}`, { params }),
  // 获取单条持仓记录
  getPosition: (userId, id) => api.get(`/api/user_position/${userId}/detail/${id}`),
  // 新增持仓记录
  addPosition: (userId, data) => api.post(`/api/user_position/${userId}`, data),
  // 更新持仓记录
  updatePosition: (userId, id, data) => api.put(`/api/user_position/${userId}/${id}`, data),
  // 删除持仓记录
  deletePosition: (userId, id) => api.delete(`/api/user_position/${userId}/${id}`),
}; 