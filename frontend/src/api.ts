import axios, { AxiosError } from 'axios';

export const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Access-Control-Allow-Origin': 'http://localhost:5173',
  },
  withCredentials: true,
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
});

// Add request interceptor to include auth token if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (email: string, password: string) => {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    return api.post('/api/users/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
  },
  
  register: (userData: {
    name: string;
    email: string;
    password: string;
    role?: string;
  }) => api.post('/api/users/register', userData),
  
  getProfile: (userId: number) =>
    api.get(`/api/users/${userId}`),
};

// Restaurants API
export const restaurantsAPI = {
  getAll: () => api.get('/api/restaurants'),
  
  getById: (id: number) => api.get(`/api/restaurants/${id}`),
  
  create: (restaurantData: {
    name: string;
    address: string;
    phone?: string;
    cuisine_type?: string;
  }) => api.post('/api/restaurants', restaurantData),
};

// Menu API
export const menuAPI = {
  getMenuItems: (restaurantId: number) => 
    api.get(`/api/menu/${restaurantId}`),
  
  getByRestaurant: (restaurantId: number) => 
    api.get(`/api/menu/${restaurantId}`),
  
  addMenuItem: (restaurantId: number, item: any) =>
    api.post(`/api/menu/${restaurantId}`, item),
  
  addItem: (restaurantId: number, item: any) =>
    api.post(`/api/menu/${restaurantId}`, item),
  
  deleteMenuItem: (itemId: number) =>
    api.delete(`/api/menu/${itemId}`),
    
  deleteItem: (itemId: number) =>
    api.delete(`/api/menu/${itemId}`)
};

// Orders API
export const ordersAPI = {
  create: (orderData: {
    customer_id: number;
    restaurant_id: number;
    total_price: number;
  }) => api.post('/api/orders', orderData),
  
  getById: (orderId: number) => api.get(`/api/orders/${orderId}`),
  
  getByCustomer: (customerId: number) =>
    api.get(`/api/orders/customer/${customerId}`),
  
  getByRestaurant: (restaurantId: number) =>
    api.get(`/api/orders/restaurant/${restaurantId}`),
  
  updateStatus: (orderId: number, status: 'placed' | 'delivered') =>
    api.patch(`/api/orders/${orderId}`, { status }),
};

export const uploadAPI = {
  uploadImage: (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/api/upload-image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }
};

export default api;
