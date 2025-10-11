import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('access_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear token and redirect to login
      if (typeof window !== 'undefined') {
        localStorage.removeItem('access_token');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// User/Auth Types
export interface UserCreate {
  username: string;
  password: string;
  email?: string;
  full_name?: string;
}

export interface UserLogin {
  username: string;
  password: string;
}

export interface UserResponse {
  id: string;
  username: string;
  email?: string;
  full_name?: string;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
  updated_at: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

// Auth API functions
export const authAPI = {
  // Register a new user
  register: async (userData: UserCreate): Promise<UserResponse> => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },

  // Login with username and password
  login: async (credentials: UserLogin): Promise<Token> => {
    const response = await api.post('/auth/login/json', credentials);
    return response.data;
  },

  // Get current user info
  getCurrentUser: async (): Promise<UserResponse> => {
    const response = await api.get('/auth/me');
    return response.data;
  },

  // Refresh token
  refreshToken: async (): Promise<Token> => {
    const response = await api.post('/auth/refresh');
    return response.data;
  },

  // Logout
  logout: async (): Promise<void> => {
    await api.post('/auth/logout');
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
    }
  },
};

// Helper functions for token management
export const tokenManager = {
  setToken: (token: string) => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', token);
    }
  },

  getToken: (): string | null => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('access_token');
    }
    return null;
  },

  removeToken: () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
    }
  },

  isAuthenticated: (): boolean => {
    return !!tokenManager.getToken();
  },
};

// Todo Types
export interface TodoCreate {
  title: string;
  description?: string;
  completed?: boolean;
  priority?: 'high' | 'medium' | 'low';
  deadline: string; // ISO date string (YYYY-MM-DD)
  labels?: string[];
  username: string;
}

export interface TodoUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
  priority?: 'high' | 'medium' | 'low';
  deadline?: string;
  labels?: string[];
}

export interface TodoResponse {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority: string;
  deadline: string;
  labels: string[];
  username: string;
  created_at: string;
  updated_at: string;
}

// Todo API functions
export const todoAPI = {
  // Create a new todo
  create: async (todo: TodoCreate): Promise<TodoResponse> => {
    const response = await api.post('/todos/', todo);
    return response.data;
  },

  // Get all todos with optional filters
  getAll: async (params?: {
    skip?: number;
    limit?: number;
    completed?: boolean;
    priority?: string;
  }): Promise<TodoResponse[]> => {
    const response = await api.get('/todos/', { params });
    return response.data;
  },

  // Get todos for a specific user
  getByUsername: async (
    username: string,
    params?: {
      skip?: number;
      limit?: number;
      completed?: boolean;
    }
  ): Promise<TodoResponse[]> => {
    const response = await api.get(`/todos/user/${username}`, { params });
    return response.data;
  },

  // Get a single todo by ID
  getById: async (todoId: string): Promise<TodoResponse> => {
    const response = await api.get(`/todos/${todoId}`);
    return response.data;
  },

  // Update a todo
  update: async (todoId: string, todo: TodoUpdate): Promise<TodoResponse> => {
    const response = await api.put(`/todos/${todoId}`, todo);
    return response.data;
  },

  // Delete a todo
  delete: async (todoId: string): Promise<void> => {
    await api.delete(`/todos/${todoId}`);
  },

  // Mark todo as complete
  markComplete: async (todoId: string): Promise<TodoResponse> => {
    const response = await api.patch(`/todos/${todoId}/complete`);
    return response.data;
  },

  // Mark todo as incomplete
  markIncomplete: async (todoId: string): Promise<TodoResponse> => {
    const response = await api.patch(`/todos/${todoId}/incomplete`);
    return response.data;
  },

  // Get todo count
  getCount: async (completed?: boolean): Promise<number> => {
    const response = await api.get('/todos/count', {
      params: completed !== undefined ? { completed } : {},
    });
    return response.data.count;
  },

  // Search todos
  search: async (
    query: string,
    params?: {
      skip?: number;
      limit?: number;
    }
  ): Promise<TodoResponse[]> => {
    const response = await api.get('/todos/search', {
      params: { q: query, ...params },
    });
    return response.data;
  },
};

export default api;

