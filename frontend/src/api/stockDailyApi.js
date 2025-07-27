import axios from 'axios';
import API_CONFIG, {ENDPOINTS} from './config';

const api = axios.create({
  baseURL: API_CONFIG.baseURL,
  timeout: API_CONFIG.timeout,
});

/**
 * 股票每日数据API
 */
export const stockDailyApi = {
  /**
   * 获取股票每日数据
   * @param {string} tsCode - 股票代码
   * @param {string} startDate - 开始日期 (YYYY-MM-DD)
   * @param {string} endDate - 结束日期 (YYYY-MM-DD)
   * @param {number} page - 页码
   * @param {number} pageSize - 每页数量
   * @returns {Promise<Object>} 包含数据和分页信息
   */
  getDailyData: async (tsCode, trade_date, startDate, endDate, page = 1, pageSize = 20, sortFields = null) => {
    try {
      const response = await api.get(ENDPOINTS.DAILY, {
        params: {
          ts_code: tsCode,
          trade_date: trade_date,
          start_date: startDate,
          end_date: endDate,
          page,
          page_size: pageSize,
          sort_fields: sortFields
        }
      });
      return response.data;
    } catch (error) {
      console.error('获取股票每日数据失败:', error);
      throw error;
    }
  },

  /**
   * 获取股票最新数据
   * @param {string} tsCode - 股票代码
   * @returns {Promise<Object>} 最新交易数据
   */
  getLatestData: async (tsCode) => {
    try {
      const response = await api.get('/stock/daily/latest', {
        params: { ts_code: tsCode }
      });
      return response.data;
    } catch (error) {
      console.error('获取最新数据失败:', error);
      throw error;
    }
  },

  /**
   * 导出股票每日数据
   * @param {string} tsCode - 股票代码
   * @param {string} startDate - 开始日期
   * @param {string} endDate - 结束日期
   * @returns {Promise<Blob>} CSV文件数据
   */
  exportDailyData: async (tsCode, startDate, endDate) => {
    try {
      const response = await api.get('/stock/daily/export', {
        params: {
          ts_code: tsCode,
          start_date: startDate,
          end_date: endDate
        },
        responseType: 'blob'
      });
      return response.data;
    } catch (error) {
      console.error('导出数据失败:', error);
      throw error;
    }
  }
};

