import axios, { AxiosResponse } from 'axios';
import { AuthResponse, LoginCredentials, RegisterCredentials, Todo, TodoCreate, TodoUpdate } from '../types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear token and redirect to login
      localStorage.removeItem('access_token');
      window.location.href = '/signin';
    }
    return Promise.reject(error);
  }
);

// Auth API calls
export const authAPI = {
  register: (credentials: RegisterCredentials): Promise<AxiosResponse<AuthResponse>> =>
    api.post('/api/auth/register', credentials),

  login: (email: string, password: string): Promise<AxiosResponse<AuthResponse>> =>
    api.post('/api/auth/login', { email, password }),

  logout: () => {
    localStorage.removeItem('access_token');
  },

  isAuthenticated: () => {
    return !!localStorage.getItem('access_token');
  }
};

// Todo API calls
export const todoAPI = {
  getAll: (): Promise<AxiosResponse<Todo[]>> =>
    api.get('/api/todos/'),

  create: (todo: TodoCreate): Promise<AxiosResponse<Todo>> =>
    api.post('/api/todos/', todo),

  update: (id: number, todo: TodoUpdate): Promise<AxiosResponse<Todo>> =>
    api.put(`/api/todos/${id}`, todo),

  delete: (id: number): Promise<AxiosResponse<void>> =>
    api.delete(`/api/todos/${id}`),

  toggleComplete: (id: number, completed: boolean): Promise<AxiosResponse<{ id: number; completed: boolean }>> =>
    api.patch(`/api/todos/${id}/status`, { completed }),

  getById: (id: number): Promise<AxiosResponse<Todo>> =>
    api.get(`/api/todos/${id}`)
};

// Define the Task type to match the backend Task model
export interface Task {
  id: string;
  title: string;
  description: string;
  status: string;
  priority: string;
  created_at: string;
  updated_at: string;
  completed_at: string | null;
}

export interface TaskCreate {
  title: string;
  description?: string;
  status?: string;
  priority?: string;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  status?: string;
  priority?: string;
}

// Task API calls
export const taskAPI = {
  getAll: (): Promise<AxiosResponse<Task[]>> =>
    api.get('/api/tasks/'),

  create: (task: TaskCreate): Promise<AxiosResponse<Task>> =>
    api.post('/api/tasks/', task),

  update: (id: string, task: TaskUpdate): Promise<AxiosResponse<Task>> =>
    api.put(`/api/tasks/${id}`, task),

  delete: (id: string): Promise<AxiosResponse<void>> =>
    api.delete(`/api/tasks/${id}`),

  toggleComplete: (id: string): Promise<AxiosResponse<Task>> =>
    api.patch(`/api/tasks/${id}/complete`),

  getById: (id: string): Promise<AxiosResponse<Task>> =>
    api.get(`/api/tasks/${id}`)
};

export default api;