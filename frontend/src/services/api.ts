// src/services/api.ts
import axios, { type AxiosResponse } from 'axios';

// Define types for tasks
export interface Task {
  id: string | number; // Backend might return string or number
  title: string;
  description?: string;
  status: 'pending' | 'completed' | 'in-progress';
  priority?: 'low' | 'medium' | 'high';
  due_date?: string; // ISO date string
  created_at?: string; // ISO date string (optional to match Todo interface)
  updated_at?: string; // ISO date string (optional to match Todo interface)
  completed_at?: string | null; // ISO date string or null
  user_id: number;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  status?: 'pending' | 'completed' | 'in-progress';
  priority?: 'low' | 'medium' | 'high';
  due_date?: string;
}

// Use the environment variable for the API base URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://fatimahnoman-phase-three.hf.space';

// Create the main API instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor to handle token refresh or errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access - maybe redirect to login
      localStorage.removeItem('access_token');
      if (typeof window !== 'undefined') {
        window.location.href = '/signin';
      }
    }
    return Promise.reject(error);
  }
);

// Define API modules
const authAPI = {
  login: async (email: string, password: string) => {
    const response = await api.post('/api/auth/login', { email, password });
    
    // Check if response.data exists and has access_token
    if (response.data && response.data.access_token) {
      const { access_token } = response.data;
      localStorage.setItem('access_token', access_token);
    } else {
      console.error('Login response does not contain access_token:', response.data);
      throw new Error('Invalid login response: access_token not found');
    }
    
    return response;
  },

  register: async (userData: { email: string; password: string }) => {
    const response = await api.post('/api/auth/register', userData);
    
    // Check if response.data exists and has access_token
    if (response.data && response.data.access_token) {
      const { access_token } = response.data;
      localStorage.setItem('access_token', access_token);
    } else {
      console.error('Registration response does not contain access_token:', response.data);
      throw new Error('Invalid registration response: access_token not found');
    }
    
    return response;
  },

  logout: () => {
    localStorage.removeItem('access_token');
  },

  isAuthenticated: () => {
    return !!localStorage.getItem('access_token');
  },
};

const todoAPI = {
  getAll: async () => {
    const response = await api.get('/api/todos');
    return response.data;
  },

  create: async (todoData: any) => {
    const response = await api.post('/api/todos', todoData);
    return response.data;
  },

  update: async (id: number, updates: any) => {
    const response = await api.put(`/api/todos/${id}`, updates);
    return response.data;
  },

  toggleComplete: async (id: number, completed: boolean) => {
    const response = await api.patch(`/api/todos/${id}`, { completed });
    return response.data;
  },

  delete: async (id: number) => {
    const response = await api.delete(`/api/todos/${id}`);
    return response.data;
  },
};

const taskAPI = {
  getAll: async () => {
    const response = await api.get('/api/tasks');
    // Return the response directly since backend returns array directly
    return response.data;
  },

  create: async (taskData: any) => {
    const response = await api.post('/api/tasks', taskData);
    return response.data;
  },

  update: async (id: string | number, updates: any) => {
    const response = await api.put(`/api/tasks/${id}`, updates);
    return response.data;
  },

  toggleComplete: async (id: string | number) => {
    const response = await api.patch(`/api/tasks/${id}/complete`);
    return response.data;
  },

  delete: async (id: string | number) => {
    const response = await api.delete(`/api/tasks/${id}`);
    return response.data;
  },
};

// Export the main API instance and modules
export { api, authAPI, todoAPI, taskAPI };


// Also export the base API instance in case it's needed directly
export default api;