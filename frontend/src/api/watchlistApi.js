import axios from 'axios';
import API_CONFIG from './config';

const api = axios.create({
  baseURL: API_CONFIG.baseURL,
  timeout: API_CONFIG.timeout,
});

/**
 * 用户关注股票API
 */
export const watchlistApi = {
  /**
   * 获取用户关注的股票列表
   * @param {number} userId - 用户ID
   * @param {Object} params - 查询参数
   * @returns {Promise<Array>} 关注的股票列表
   */
  getUserWatchlist: async (userId, params = {}) => {
    try {
      userId = 1;
      const response = await api.get(`/api/user_stock/${userId}`, { params });
      return response.data;
    } catch (error) {
      console.error('获取关注列表失败:', error);
      throw error;
    }
  },

  /**
   * 添加股票到关注列表
   * @param {number} userId - 用户ID
   * @param {string} tsCode - 股票代码
   * @returns {Promise<Object>} 操作结果
   */
  addToWatchlist: async (userId, tsCode) => {
    try {
      userId = 1;
      const response = await api.post(`/api/user_stock/`, {
        user_id: userId,
        ts_code: tsCode
      });
      return response.data;
    } catch (error) {
      console.error('添加关注失败:', error);
      throw error;
    }
  },

  /**
   * 从关注列表中移除股票
   * @param {number} userId - 用户ID
   * @param {string} tsCode - 股票代码
   * @returns {Promise<Object>} 操作结果
   */
  removeFromWatchlist: async (userId, tsCode) => {
    try {
      userId = 1;
      const response = await api.delete(`/api/user_stock/${userId}/${tsCode}`);
      return response.data;
    } catch (error) {
      console.error('移除关注失败:', error);
      throw error;
    }
  },

  /**
   * 检查股票是否在关注列表中
   * @param {number} userId - 用户ID
   * @param {string} tsCode - 股票代码
   * @returns {Promise<boolean>} 是否已关注
   */
  isInWatchlist: async (userId, tsCode) => {
    try {
      userId = 1;
      const response = await api.get(`/api/user_stock/${userId}/${tsCode}`);
      return response.data.ts_code != null;
    } catch (error) {
      console.error('检查关注状态失败:', error);
      return false;
    }
  },

  /**
   * 修改股票评级
   * @param {number} userId - 用户ID
   * @param {string} tsCode - 股票代码
   * @param {string|number} rating - 评级
   * @returns {Promise<Object>} 操作结果
   */
  updateStockRating: async (userId, tsCode, rating) => {
    try {
      userId = 1;
      const response = await api.put(`/api/user_stock/${userId}/${tsCode}/rating`, { rating });
      return response.data;
    } catch (error) {
      console.error('修改股票评级失败:', error);
      throw error;
    }
  }
};