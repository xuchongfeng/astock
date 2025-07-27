import axios from 'axios';
import API_CONFIG, { ENDPOINTS } from './config';

const api = axios.create({
  baseURL: API_CONFIG.baseURL,
  timeout: API_CONFIG.timeout,
});

/**
 * 行业统计数据API模块
 */
export const industryStatsApi = {
  /**
   * 获取行业统计数据
   * @param {number} industryId - 行业ID
   * @param {string} startDate - 开始日期 (YYYY-MM-DD)
   * @param {string} endDate - 结束日期 (YYYY-MM-DD)
   * @returns {Promise<Array>} 行业统计数据
   */
  getIndustryStats: async (industryId, startDate, endDate) => {
    try {
      const response = await api.get(ENDPOINTS.INDUSTRY_STATS, {
        params: {
          industry_id: industryId,
          start_date: startDate,
          end_date: endDate
        }
      });
      return response.data;
    } catch (error) {
      console.error('获取行业统计数据失败:', error);
      throw error;
    }
  },

  /**
   * 获取行业最新统计数据
   * @param {number} industryId - 行业ID
   * @returns {Promise<Object>} 最新行业统计数据
   */
  getLatestIndustryStats: async (industryId) => {
    try {
      const response = await api.get(`${ENDPOINTS.INDUSTRY_STATS}/`, {
        params: { industry_id: industryId }
      });
      return response.data;
    } catch (error) {
      console.error('获取最新行业统计数据失败:', error);
      throw error;
    }
  },

  /**
   * 获取多个行业对比数据
   * @param {Array<number>} industryIds - 行业ID数组
   * @param {string} metric - 对比指标 (total_amount/up_count/down_count)
   * @param {string} startDate - 开始日期
   * @param {string} endDate - 结束日期
   * @returns {Promise<Object>} 行业对比数据
   */
  getIndustryComparison: async (industryIds, metric, startDate, endDate) => {
    try {
      const response = await api.get(`${ENDPOINTS.INDUSTRY_STATS}/comparison`, {
        params: {
          industry_ids: industryIds.join(','),
          metric,
          start_date: startDate,
          end_date: endDate
        }
      });
      return response.data;
    } catch (error) {
      console.error('获取行业对比数据失败:', error);
      throw error;
    }
  },

  /**
   * 获取行业趋势数据
   * @param {number} industryId - 行业ID
   * @param {string} metric - 指标类型 (total_amount/up_count/down_count)
   * @param {string} period - 周期 (daily/weekly/monthly)
   * @returns {Promise<Array>} 行业趋势数据
   */
  getIndustryTrend: async (industryId, metric, period = 'daily') => {
    try {
      const response = await api.get(`${ENDPOINTS.INDUSTRY_STATS}/trend`, {
        params: {
          industry_id: industryId,
          metric,
          period
        }
      });
      return response.data;
    } catch (error) {
      console.error('获取行业趋势数据失败:', error);
      throw error;
    }
  },

  /**
   * 获取行业排行榜单
   * @param {string} metric - 排名指标 (total_amount/up_count/down_count)
   * @param {string} date - 统计日期
   * @param {number} limit - 返回数量
   * @returns {Promise<Array>} 行业排名数据
   */
  getIndustryRanking: async (metric, date, limit = 40) => {
    try {
      const response = await api.get(`${ENDPOINTS.INDUSTRY_STATS}/`, {
        params: {
          "sort_fields": metric,
          "state_date": date,
          "page_size": limit
        }
      });
      return response.data;
    } catch (error) {
      console.error('获取行业排行榜单失败:', error);
      throw error;
    }
  }
};