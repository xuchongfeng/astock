import axios from 'axios';
import API_CONFIG from './config';

const api = axios.create({
  baseURL: API_CONFIG.baseURL,
  timeout: API_CONFIG.timeout,
});

/**
 * 文章API模块
 * 提供文章相关的接口调用
 */
export const articleApi = {
  /**
   * 获取文章列表
   * @param {Object} params - 查询参数
   * @returns {Promise<Object>} 文章列表
   */
  getArticles: async (params = {}) => {
    try {
      const response = await api.get('/api/articles', { params });
      return response.data;
    } catch (error) {
      console.error('获取文章列表失败:', error);
      throw error;
    }
  },

  /**
   * 获取单篇文章
   * @param {number} articleId - 文章ID
   * @returns {Promise<Object>} 文章详情
   */
  getArticle: async (articleId) => {
    try {
      const response = await api.get(`/api/articles/${articleId}`);
      return response.data;
    } catch (error) {
      console.error('获取文章详情失败:', error);
      throw error;
    }
  },

  /**
   * 创建文章
   * @param {Object} articleData - 文章数据
   * @returns {Promise<Object>} 创建的文章
   */
  createArticle: async (articleData) => {
    try {
      const response = await api.post('/api/articles', articleData);
      return response.data;
    } catch (error) {
      console.error('创建文章失败:', error);
      throw error;
    }
  },

  /**
   * 更新文章
   * @param {number} articleId - 文章ID
   * @param {Object} articleData - 更新数据
   * @returns {Promise<Object>} 更新后的文章
   */
  updateArticle: async (articleId, articleData) => {
    try {
      const response = await api.put(`/api/articles/${articleId}`, articleData);
      return response.data;
    } catch (error) {
      console.error('更新文章失败:', error);
      throw error;
    }
  },

  /**
   * 删除文章
   * @param {number} articleId - 文章ID
   * @returns {Promise<Object>} 删除结果
   */
  deleteArticle: async (articleId) => {
    try {
      const response = await api.delete(`/api/articles/${articleId}`);
      return response.data;
    } catch (error) {
      console.error('删除文章失败:', error);
      throw error;
    }
  },

  /**
   * 点赞文章
   * @param {number} articleId - 文章ID
   * @returns {Promise<Object>} 点赞结果
   */
  likeArticle: async (articleId) => {
    try {
      const response = await api.post(`/api/articles/${articleId}/like`);
      return response.data;
    } catch (error) {
      console.error('点赞文章失败:', error);
      throw error;
    }
  },

  /**
   * 获取用户文章
   * @param {number} userId - 用户ID
   * @param {string} status - 状态过滤
   * @returns {Promise<Object>} 用户文章列表
   */
  getUserArticles: async (userId, status = null) => {
    try {
      const params = {};
      if (status) params.status = status;
      
      const response = await api.get(`/api/articles/user/${userId}`, { params });
      return response.data;
    } catch (error) {
      console.error('获取用户文章失败:', error);
      throw error;
    }
  },

  /**
   * 获取公开文章
   * @param {Object} params - 查询参数
   * @returns {Promise<Object>} 公开文章列表
   */
  getPublicArticles: async (params = {}) => {
    try {
      const response = await api.get('/api/articles/public', { params });
      return response.data;
    } catch (error) {
      console.error('获取公开文章失败:', error);
      throw error;
    }
  },

  /**
   * 获取用户文章统计
   * @param {number} userId - 用户ID
   * @returns {Promise<Object>} 文章统计信息
   */
  getUserArticleStatistics: async (userId) => {
    try {
      const response = await api.get(`/api/articles/user/${userId}/statistics`);
      return response.data;
    } catch (error) {
      console.error('获取用户文章统计失败:', error);
      throw error;
    }
  }
};
