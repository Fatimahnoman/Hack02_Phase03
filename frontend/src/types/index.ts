export interface User {
  id: number;
  email: string;
  created_at: string;
  updated_at: string;
}

export interface Todo {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  due_date?: string; // Optional due date
  user_id: number;
  created_at?: string; // Optional to allow for new todos that haven't been saved yet
  updated_at?: string; // Optional to allow for new todos that haven't been saved yet
}

export interface TodoCreate {
  title: string;
  description?: string;
  due_date?: string; // Optional due date
}

export interface TodoUpdate {
  title?: string;
  description?: string;
  due_date?: string;
  completed?: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterCredentials {
  email: string;
  password: string;
}