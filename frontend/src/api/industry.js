import axios from 'axios';

const BASE_URL = '/api/industry';

export const fetchIndustries = (params) => axios.get(`${BASE_URL}/`, { params });
export const fetchIndustryById = (id) => axios.get(`${BASE_URL}/${id}`);
export const createIndustry = (data) => axios.post(`${BASE_URL}/`, data);
export const updateIndustry = (id, data) => axios.put(`${BASE_URL}/${id}`, data);
export const deleteIndustry = (id) => axios.delete(`${BASE_URL}/${id}`);
