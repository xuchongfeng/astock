import axios from 'axios';
import API_CONFIG from './config';

const api = axios.create({
  baseURL: API_CONFIG.baseURL,
  timeout: API_CONFIG.timeout,
});

/**
 * 指数数据API模块
 * 提供与指数相关数据的获取接口
 */
export const indexApi = {
  /**
   * 获取指数每日数据
   * @param {string} tsCode - 指数代码 (如: 000001.SH)
   * @param {string} startDate - 开始日期 (YYYY-MM-DD)
   * @param {string} endDate - 结束日期 (YYYY-MM-DD)
   * @returns {Promise<Object>} 指数每日数据
   */
  getIndexDaily: async (tsCode, startDate, endDate) => {
    try {
      const response = await api.get(`/index_daily/${tsCode}/range`, {
        params: {
          start_date: startDate,
          end_date: endDate
        }
      });
      return response.data;
    } catch (error) {
      console.error('获取指数每日数据失败:', error);
      throw error;
    }
  },

  /**
   * 获取指数最新数据
   * @param {string} tsCode - 指数代码
   * @returns {Promise<Object>} 最新数据
   */
  getIndexLatest: async (tsCode) => {
    try {
      const response = await api.get(`/index_daily/${tsCode}/latest`);
      return response.data;
    } catch (error) {
      console.error('获取指数最新数据失败:', error);
      throw error;
    }
  },

  /**
   * 获取指数统计信息
   * @param {string} tsCode - 指数代码
   * @param {number} days - 统计天数
   * @returns {Promise<Object>} 统计信息
   */
  getIndexStatistics: async (tsCode, days = 30) => {
    try {
      const response = await api.get(`/index_daily/${tsCode}/statistics`, {
        params: { days }
      });
      return response.data;
    } catch (error) {
      console.error('获取指数统计信息失败:', error);
      throw error;
    }
  },

  /**
   * 获取多个指数的数据
   * @param {Array} tsCodes - 指数代码数组
   * @param {string} startDate - 开始日期
   * @param {string} endDate - 结束日期
   * @returns {Promise<Object>} 多个指数的数据
   */
  getMultipleIndexData: async (tsCodes, startDate, endDate) => {
    try {
      const promises = tsCodes.map(tsCode => 
        indexApi.getIndexDaily(tsCode, startDate, endDate)
      );
      const results = await Promise.all(promises);
      
      return {
        code: 200,
        message: '获取成功',
        data: results.map((result, index) => ({
          ts_code: tsCodes[index],
          data: result.data || []
        }))
      };
    } catch (error) {
      console.error('获取多个指数数据失败:', error);
      throw error;
    }
  }
};

