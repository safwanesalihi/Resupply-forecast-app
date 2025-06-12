import axios from 'axios';

// Determine API URL based on environment
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

console.log("API URL:", API_URL); // Log the API URL being used

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken'); // Use a consistent key like 'authToken'
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add response interceptor for handling common errors (e.g., 401 Unauthorized)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Handle unauthorized access, e.g., redirect to login
      console.error("Unauthorized access - redirecting to login");
      localStorage.removeItem('authToken');
      // window.location.href = '/login'; // Uncomment if you have a login route
    }
    return Promise.reject(error);
  }
);


// Auth API
export const authAPI = {
  login: async (username, password) => {
    // FastAPI's OAuth2PasswordRequestForm expects form data
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    const response = await axios.post(`${API_URL}/auth/login`, formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    // Save token upon successful login
    if (response.data.access_token) {
      localStorage.setItem('authToken', response.data.access_token);
    }
    return response.data; // Should return { access_token: string, token_type: string }
  },

  register: async (userData) => {
    const response = await api.post('/auth/register', userData);
    return response.data; // Should return the created user object
  },

  // Optional: Add a function to get the current user's profile
  getCurrentUser: async () => {
      // Assuming you have a /users/me endpoint protected by auth
      // This requires a separate endpoint in the backend (not shown in previous steps)
      // Example:
      // const response = await api.get('/users/me');
      // return response.data;
      return Promise.resolve(null); // Placeholder
  }
};

// Products API
export const productsAPI = {
  getProducts: async (params = {}) => {
    const response = await api.get('/products', { params });
    return response.data;
  },

  getProduct: async (id) => {
    const response = await api.get(`/products/${id}`);
    return response.data;
  },

  createProduct: async (productData) => {
    const response = await api.post('/products', productData);
    return response.data;
  },

  updateProduct: async (id, productData) => {
    const response = await api.put(`/products/${id}`, productData);
    return response.data;
  },

  deleteProduct: async (id) => {
    const response = await api.delete(`/products/${id}`);
    return response.data;
  },
};

// Sales API
export const salesAPI = {
  getRawSales: async (params = {}) => {
    const response = await api.get('/sales/raw', { params });
    return response.data;
  },

  getCleanSales: async (params = {}) => {
    const response = await api.get('/sales/clean', { params });
    return response.data;
  },

  importSales: async (importData) => {
    const response = await api.post('/sales/import', importData);
    return response.data;
  },
};

// Forecasts API
export const forecastsAPI = {
  getForecasts: async (params = {}) => {
    const response = await api.get('/forecasts', { params });
    return response.data;
  },

  getProductForecast: async (productId, params = {}) => {
    const response = await api.get(`/forecasts/${productId}`, { params });
    return response.data;
  },

  generateForecasts: async (forecastParams) => {
    const response = await api.post('/forecasts/generate', forecastParams);
    return response.data;
  },
  
  // New method to get Prophet forecasts
  getProphetForecast: async () => {
    const response = await api.get('/forecasts/prophet/forecast');
    return response.data;
  },
};

// Alerts API
export const alertsAPI = {
  getAlerts: async (params = {}) => {
    const response = await api.get('/alerts', { params });
    return response.data;
  },

  checkAlerts: async () => {
    const response = await api.get('/alerts/check');
    return response.data;
  },

  updateAlertStatus: async (alertId, status) => {
    const response = await api.put(`/alerts/${alertId}/status`, { status });
    return response.data;
  },
};

export default api;

