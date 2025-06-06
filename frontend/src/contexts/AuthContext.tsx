import React, { createContext, useState, useContext, useEffect, ReactNode } from 'react';
import { authAPI } from '../services/api'; // Assuming your API service is here

// Define the shape of the context data
interface AuthContextType {
  token: string | null;
  user: any | null; // Replace 'any' with a proper User type if available
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  register: (userData: any) => Promise<any>; // Replace 'any' with specific types
}

// Create the context with a default value
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Define the props for the provider component
interface AuthProviderProps {
  children: ReactNode;
}

// Create the provider component
export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [token, setToken] = useState<string | null>(localStorage.getItem('authToken'));
  const [user, setUser] = useState<any | null>(null); // Store user info if needed
  const [isLoading, setIsLoading] = useState<boolean>(true); // Start loading until token/user checked

  useEffect(() => {
    // Check if token exists on initial load
    const checkUser = async () => {
      const storedToken = localStorage.getItem('authToken');
      if (storedToken) {
        setToken(storedToken);
        // Optional: Fetch user profile based on token
        // try {
        //   const currentUser = await authAPI.getCurrentUser(); // Implement this in api.ts
        //   setUser(currentUser);
        // } catch (error) {
        //   console.error("Failed to fetch user on load", error);
        //   localStorage.removeItem('authToken'); // Token might be invalid
        //   setToken(null);
        // }
      } else {
        setToken(null);
        setUser(null);
      }
      setIsLoading(false);
    };
    checkUser();
  }, []);

  const login = async (username: string, password: string) => {
    try {
      setIsLoading(true);
      const data = await authAPI.login(username, password);
      if (data.access_token) {
        setToken(data.access_token);
        localStorage.setItem('authToken', data.access_token);
        // Optional: Fetch user profile after login
        // const currentUser = await authAPI.getCurrentUser();
        // setUser(currentUser);
      } else {
        throw new Error('Login failed: No access token received');
      }
      setIsLoading(false);
    } catch (error) {
      console.error("Login error:", error);
      setIsLoading(false);
      // Re-throw the error so the calling component can handle it (e.g., show error message)
      throw error;
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('authToken');
    // Optionally redirect to login page
    // window.location.href = '/login';
  };

  const register = async (userData: any) => {
    try {
        setIsLoading(true);
        const registeredUser = await authAPI.register(userData);
        setIsLoading(false);
        return registeredUser; // Return user data upon successful registration
    } catch (error) {
        console.error("Registration error:", error);
        setIsLoading(false);
        throw error; // Re-throw for component handling
    }
  };

  // Value provided to consuming components
  const value = {
    token,
    user,
    isLoading,
    login,
    logout,
    register
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Custom hook to use the AuthContext
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

