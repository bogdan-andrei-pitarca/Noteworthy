import { API_BASE_URL } from './apiConfig';

export const authService = {
    async register(credentials: { email: string; password: string }) {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(credentials)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: 'Registration failed' }));
            throw new Error(errorData.detail || `Error ${response.status}`);
        }
        return response.json(); 
    },

    async login(credentials: { email: string; password: string }) {
        const formData = new URLSearchParams();
        formData.append('username', credentials.email); 
        formData.append('password', credentials.password);

        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData.toString()
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: 'Login failed' }));
            throw new Error(errorData.detail || `Error ${response.status}`);
        }
        return response.json(); 
    }
};