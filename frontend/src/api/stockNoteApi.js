import axios from 'axios';
import API_CONFIG from './config';

const api = axios.create({
  baseURL: API_CONFIG.baseURL,
  timeout: API_CONFIG.timeout,
});

export const stockNoteApi = {
  // 获取股票记录列表
  getNotes: (params = {}) => api.get('/api/stock_note', { params }),

  // 获取单条记录
  getNote: (id) => api.get(`/api/stock_note/${id}`),

  // 新增记录
  addNote: (data) => api.post('/api/stock_note', data),

  // 更新记录
  updateNote: (id, data) => api.put(`/api/stock_note/${id}`, data),

  // 删除记录
  deleteNote: (id) => api.delete(`/api/stock_note/${id}`),
}; 