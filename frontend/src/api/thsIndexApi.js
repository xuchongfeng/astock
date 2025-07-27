import axios from 'axios';
import API_CONFIG from './config';

const api = axios.create({
  baseURL: API_CONFIG.baseURL,
  timeout: API_CONFIG.timeout,
});

export const thsIndexApi = {
  // 获取指数行情列表
  getList: (params = {}) => api.get('/api/ths_index_daily', { params }),

  // 获取单条指数行情
  getById: (id) => api.get(`/api/ths_index_daily/${id}`),

  // 按ts_code和日期查询
  getByTsCodeAndDate: (ts_code, trade_date) => api.get('/api/ths_index_daily/query', { params: { ts_code, trade_date } }),
}; 