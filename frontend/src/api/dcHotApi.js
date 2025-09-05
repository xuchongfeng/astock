import axios from 'axios';
import API_CONFIG from './config';

const api = axios.create({
  baseURL: API_CONFIG.baseURL,
  timeout: API_CONFIG.timeout,
});

const BASE_URL = '/api/dc_hot';

// 东方财富热榜API
export const dcHotApi = {
  // 获取热榜数据列表
  getDcHotList: (params) => {
    return api.get(`${BASE_URL}/list`, { params });
  },

  // 获取最新热榜数据
  getLatestDcHot: (params) => {
    return api.get(`${BASE_URL}/latest`, { params });
  },

  // 获取市场类型列表
  getMarkets: () => {
    return api.get(`${BASE_URL}/markets`);
  },

  // 获取热点类型列表
  getHotTypes: () => {
    return api.get(`${BASE_URL}/hot_types`);
  },

  // 创建热榜数据
  createDcHot: (data) => {
    return api.post(BASE_URL, data);
  },

  // 更新热榜数据
  updateDcHot: (id, data) => {
    return api.put(`${BASE_URL}/${id}`, data);
  },

  // 删除热榜数据
  deleteDcHot: (id) => {
    return api.delete(`${BASE_URL}/${id}`);
  },

  // 根据ID获取热榜数据
  getDcHotById: (id) => {
    return api.get(`${BASE_URL}/${id}`);
  }
};
