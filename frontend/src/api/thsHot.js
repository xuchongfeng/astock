import axios from 'axios';
import API_CONFIG from './config';

const api = axios.create({
  baseURL: API_CONFIG.baseURL,
  timeout: API_CONFIG.timeout,
});

const BASE_URL = '/api/ths_hot';

// 获取热榜数据列表
export const fetchHotDataList = (params = {}) => {
  return api.get(BASE_URL, { params });
};

// 根据ID获取热榜数据
export const fetchHotDataById = (id) => {
  return api.get(`${BASE_URL}/${id}`);
};

// 创建热榜数据
export const createHotData = (data) => {
  return api.post(BASE_URL, data);
};

// 更新热榜数据
export const updateHotData = (id, data) => {
  return api.put(`${BASE_URL}/${id}`, data);
};

// 删除热榜数据
export const deleteHotData = (id) => {
  return api.delete(`${BASE_URL}/${id}`);
};

// 获取最新热榜数据
export const fetchLatestHotData = (params = {}) => {
  return api.get(`${BASE_URL}/latest`, { params });
};

// 根据日期和类型获取热榜数据
export const fetchHotDataByDateType = (tradeDate, dataType) => {
  return api.get(`${BASE_URL}/by-date-type`, {
    params: { trade_date: tradeDate, data_type: dataType }
  });
};

// 根据股票代码获取热榜历史数据
export const fetchHotDataByTsCode = (tsCode, params = {}) => {
  return api.get(`${BASE_URL}/by-ts-code/${tsCode}`, { params });
};

// 获取热榜数据统计信息
export const fetchHotDataStatistics = (params = {}) => {
  return api.get(`${BASE_URL}/statistics`, { params });
};

// 获取所有数据类型
export const fetchDataTypes = () => {
  return api.get(`${BASE_URL}/types`);
}; 