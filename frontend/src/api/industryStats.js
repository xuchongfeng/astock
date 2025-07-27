import axios from 'axios';

const BASE_URL = '/api/industry_stats';

export const fetchIndustryStats = (params) => axios.get(`${BASE_URL}/`, { params });
export const fetchIndustryStatsById = (id) => axios.get(`${BASE_URL}/${id}`);
export const createIndustryStats = (data) => axios.post(`${BASE_URL}/`, data);
export const updateIndustryStats = (id, data) => axios.put(`${BASE_URL}/${id}`, data);
export const deleteIndustryStats = (id) => axios.delete(`${BASE_URL}/${id}`);
