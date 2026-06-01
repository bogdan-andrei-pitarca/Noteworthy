"use client";

import React, { createContext, useState, useEffect, ReactNode, useContext } from 'react';
import toast from 'react-hot-toast';

interface AuthContextType {
    isAuthenticated: boolean;
    token: string | null;
    login: (token: string) => void;
    logout: () => void;
    isLoading: boolean;
}

// create context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({children }: {children: ReactNode}) => {
    const [token, setToken] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);

    // run once on mount to check for existing token
    useEffect(() => {
        const storedToken = localStorage.getItem('noteworthy_token');
        if (storedToken) {
            setToken(storedToken);
            setIsAuthenticated(true);
        }
        setIsLoading(false);
    }, []);

    const login = (newToken: string) => {
        localStorage.setItem('noteworthy_token', newToken);
        setToken(newToken);
        setIsAuthenticated(true);
        toast.success('Logged in successfully.');
    };

    const logout = () => {
        localStorage.removeItem('noteworthy_token');
        setToken(null);
        setIsAuthenticated(false);
        toast.success('Logged out successfully.');
    };

    return (
        <AuthContext.Provider value={{ isAuthenticated, token, login, logout, isLoading }}>
            {children}
        </AuthContext.Provider>
    );
};

// custom hook to grab auth state
export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};