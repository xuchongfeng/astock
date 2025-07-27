import axios from 'axios';
import API_CONFIG, { ENDPOINTS } from './config';

const api = axios.create({
  baseURL: API_CONFIG.baseURL,
  timeout: API_CONFIG.timeout,
});

export const stockApi = {
  // 获取公司列表
  getCompanies: (params = {}) => api.get(ENDPOINTS.COMPANY, { params }),

  // 获取单个公司详情
  getCompany: (id) => api.get(`${ENDPOINTS.COMPANY}/${id}`),

  // 获取股票日线数据
  getDailyData: (tsCode, startDate, endDate) =>
    api.get(ENDPOINTS.DAILY, {
      params: {
        ts_code: tsCode,
        start_date: startDate,
        end_date: endDate
      }
    }),

  // 搜索公司
  searchCompanies: (query) =>
    api.get(`${ENDPOINTS.COMPANY}/search`, { params: { q: query } }),
};