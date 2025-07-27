import axios from 'axios';
import API_CONFIG, { ENDPOINTS } from './config';

const api = axios.create({
  baseURL: API_CONFIG.baseURL,
  timeout: API_CONFIG.timeout,
});

/**
 * 行业数据API模块
 * 提供与行业相关数据的获取接口
 */
export const industryApi = {
  /**
   * 获取所有行业分类列表
   * @returns {Promise<Array>} 行业列表
   */
  getAllIndustries: async () => {
    try {
      const params = {
        "page_size": 500
      }
      const response = await api.get(ENDPOINTS.INDUSTRY, {params});
      return response.data;
    } catch (error) {
      console.error('获取行业列表失败:', error);
      throw error;
    }
  },

  /**
   * 获取特定行业的统计数据
   * @param {number} industryId - 行业ID
   * @param {string} [startDate] - 开始日期 (YYYY-MM-DD)
   * @param {string} [endDate] - 结束日期 (YYYY-MM-DD)
   * @param {string} [period] - 统计周期 (daily/weekly/monthly)
   * @returns {Promise<Array>} 行业统计数据
   */
  getIndustryStats: async (industryId, startDate, endDate, period = 'daily') => {
    try {
      const params = {
        industry_id: industryId,
        period,
        ...(startDate && { start_date: startDate }),
        ...(endDate && { end_date: endDate })
      };

      const response = await api.get(ENDPOINTS.INDUSTRY_STATS, { params });
      return response.data;
    } catch (error) {
      console.error('获取行业统计数据失败:', error);
      throw error;
    }
  },

  /**
   * 获取多个行业的对比数据
   * @param {Array<number>} industryIds - 行业ID数组
   * @param {string} metric - 对比指标 (company_count/total_amount/up_count)
   * @param {string} [startDate] - 开始日期
   * @param {string} [endDate] - 结束日期
   * @returns {Promise<Object>} 行业对比数据
   */
  getIndustryComparison: async (industryIds, metric, startDate, endDate) => {
    try {
      const params = {
        industry_ids: industryIds.join(','),
        metric,
        ...(startDate && { start_date: startDate }),
        ...(endDate && { end_date: endDate })
      };

      const response = await api.get(`${ENDPOINTS.INDUSTRY}/comparison`, { params });
      return response.data;
    } catch (error) {
      console.error('获取行业对比数据失败:', error);
      throw error;
    }
  },

  /**
   * 获取行业下的公司列表
   * @param {number} industryId - 行业ID
   * @param {number} [page=1] - 页码
   * @param {number} [pageSize=20] - 每页数量
   * @returns {Promise<Object>} 公司列表及分页信息
   */
  getCompaniesInIndustry: async (industryId, page = 1, pageSize = 20) => {
    try {
      const response = await api.get(`${ENDPOINTS.INDUSTRY}/${industryId}/companies`, {
        params: { page, page_size: pageSize }
      });
      return response.data;
    } catch (error) {
      console.error('获取行业公司列表失败:', error);
      throw error;
    }
  },

  /**
   * 获取行业历史趋势数据
   * @param {number} industryId - 行业ID
   * @param {string} metric - 指标类型 (company_count/total_amount/up_count)
   * @param {string} [range] - 时间范围 (1m/3m/6m/1y/3y/5y)
   * @returns {Promise<Array>} 时间序列数据
   */
  getIndustryTrend: async (industryId, metric, range = '1y') => {
    try {
      const response = await api.get(`${ENDPOINTS.INDUSTRY}/${industryId}/trend`, {
        params: { metric, range }
      });
      return response.data;
    } catch (error) {
      console.error('获取行业趋势数据失败:', error);
      throw error;
    }
  },

  /**
   * 获取行业排行榜单
   * @param {string} type - 榜单类型 (performance/capitalization/growth)
   * @param {string} [timeRange] - 时间范围 (today/week/month/quarter)
   * @param {number} [limit=10] - 排名数量限制
   * @returns {Promise<Array>} 行业排名数据
   */
  getIndustryRanking: async (type, timeRange = 'week', limit = 10) => {
    try {
      const response = await api.get(`${ENDPOINTS.INDUSTRY}/ranking`, {
        params: { type, time_range: timeRange, limit }
      });
      return response.data;
    } catch (error) {
      console.error('获取行业排行榜单失败:', error);
      throw error;
    }
  },

  /**
   * 获取行业历史指标热力图数据
   * @param {string} metric - 指标类型 (pct_chg/turnover_rate)
   * @param {string} [period] - 周期 (daily/weekly/monthly)
   * @param {string} [startDate] - 开始日期
   * @param {string} [endDate] - 结束日期
   * @returns {Promise<Object>} 热力图数据格式
   */
  getIndustryHeatmap: async (metric, period, startDate, endDate) => {
    try {
      const params = {
        metric,
        ...(period && { period }),
        ...(startDate && { start_date: startDate }),
        ...(endDate && { end_date: endDate })
      };

      const response = await api.get(`${ENDPOINTS.INDUSTRY}/heatmap`, { params });
      return response.data;
    } catch (error) {
      console.error('获取行业热力图数据失败:', error);
      throw error;
    }
  }
};

export default industryApi;