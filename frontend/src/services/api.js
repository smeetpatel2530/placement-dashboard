import axios from 'axios'

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000',
    timeout: 10000,
})

export const getStats = () => api.get('/api/stats')
export const getDepartments = () => api.get('/api/departments')
export const getCompanies = () => api.get('/api/companies')
export const getTimeline = () => api.get('/api/timeline')
export const getCTCDistribution = () => api.get('/api/ctc-distribution')
export const getRoles = () => api.get('/api/roles')
export const getStudents = (params = {}) => api.get('/api/students', { params })

export default api