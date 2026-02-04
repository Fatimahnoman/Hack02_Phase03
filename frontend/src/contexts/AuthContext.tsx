import React, { useState, useEffect, createContext, ReactNode } from 'react';
import { authAPI } from '../services/api';
import { User } from '../types';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  register: (email: string, password: string) => Promise<void>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in on initial load
    const token = localStorage.getItem('access_token');
    if (token && authAPI.isAuthenticated()) {
      // In a real app, you would fetch user details here
      // For now, we'll simulate restoring user data from token
      // We'll use a dummy user since we don't have a user profile endpoint
      const email = localStorage.getItem('user_email') || 'user@example.com'; // Store email when logging in
      setUser({
        id: 1,
        email,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      });
    }
    setLoading(false);
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const response = await authAPI.login(email, password);
      const { access_token } = response.data;

      localStorage.setItem('access_token', access_token);
      localStorage.setItem('user_email', email); // Store email for restoration

      // In a real app, you would fetch user details here
      // For now, we'll just set a dummy user
      setUser({ id: 1, email, created_at: new Date().toISOString(), updated_at: new Date().toISOString() });
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  };

  const register = async (email: string, password: string) => {
    try {
      const response = await authAPI.register({ email, password });
      const { access_token } = response.data;

      localStorage.setItem('access_token', access_token);
      localStorage.setItem('user_email', email); // Store email for restoration

      // In a real app, you would fetch user details here
      // For now, we'll just set a dummy user
      setUser({ id: 1, email, created_at: new Date().toISOString(), updated_at: new Date().toISOString() });
    } catch (error) {
      console.error('Registration failed:', error);
      throw error;
    }
  };

  const logout = () => {
    authAPI.logout();
    setUser(null);
  };

  const value = {
    user,
    loading,
    login,
    logout,
    register,
    isAuthenticated: !!user,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = React.useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};