'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authAPI, tokenManager, UserResponse } from '@/lib/api';
import { useRouter } from 'next/navigation';

interface AuthContextType {
  user: UserResponse | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, password: string, email?: string, full_name?: string) => Promise<void>;
  logout: () => Promise<void>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<UserResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check if user is logged in on mount
    const initAuth = async () => {
      const token = tokenManager.getToken();
      if (token) {
        try {
          const userData = await authAPI.getCurrentUser();
          setUser(userData);
        } catch (error) {
          console.error('Failed to get current user:', error);
          tokenManager.removeToken();
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const login = async (username: string, password: string) => {
    try {
      const tokenData = await authAPI.login({ username, password });
      tokenManager.setToken(tokenData.access_token);
      
      // Get user data
      const userData = await authAPI.getCurrentUser();
      setUser(userData);
      
      router.push('/welcome');
    } catch (error: any) {
      console.error('Login failed:', error);
      throw new Error(error.response?.data?.detail || 'Login failed');
    }
  };

  const register = async (username: string, password: string, email?: string, full_name?: string) => {
    try {
      await authAPI.register({ username, password, email, full_name });
      // Auto login after registration
      await login(username, password);
    } catch (error: any) {
      console.error('Registration failed:', error);
      // Preserve the full error object including response data and status
      const enhancedError = new Error(error.response?.data?.detail || error.message || 'Registration failed');
      // Attach the response object for detailed error parsing
      (enhancedError as any).response = error.response;
      throw enhancedError;
    }
  };

  const logout = async () => {
    try {
      await authAPI.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setUser(null);
      tokenManager.removeToken();
      router.push('/login');
    }
  };

  const value = {
    user,
    loading,
    login,
    register,
    logout,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

