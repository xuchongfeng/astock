import axios from 'axios';
import API_CONFIG from './config';

const api = axios.create({
  baseURL: API_CONFIG.baseURL,
  timeout: API_CONFIG.timeout,
});

export const thsMemberApi = {
  // 获取概念成分股列表
  getList: (params = {}) => api.get('/api/ths_member', { params }),

  // 获取单条概念成分股
  getById: (id) => api.get(`/api/ths_member/${id}`),

  // 按概念板块代码查询成分股
  getByTsCode: (ts_code, params = {}) => api.get('/api/ths_member', { 
    params: { ts_code, ...params } 
  }),

  // 按股票代码查询所属概念板块
  getByConCode: (con_code, params = {}) => api.get('/api/ths_member', { 
    params: { con_code, ...params } 
  }),
}; 