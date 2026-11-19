import axios from 'axios';

// Format API Base URL cleanly for local development and Render deployment
let rawUrl = import.meta.env.VITE_API_URL || '/api';
let API_BASE_URL = rawUrl.trim();

if (API_BASE_URL && !API_BASE_URL.startsWith('http') && !API_BASE_URL.startsWith('/')) {
  API_BASE_URL = `https://${API_BASE_URL}`;
}

if (API_BASE_URL.startsWith('http') && !API_BASE_URL.endsWith('/api')) {
  API_BASE_URL = `${API_BASE_URL}/api`;
}

const API = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor: attach JWT token
API.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('agrilink_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor: handle 401 unauth
API.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('agrilink_token');
      localStorage.removeItem('agrilink_user');
    }
    return Promise.reject(error);
  }
);

export default API;
