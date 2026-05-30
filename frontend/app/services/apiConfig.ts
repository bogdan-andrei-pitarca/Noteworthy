export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export const getAuthHeaders = () => {
    // Grab the token from localStorage if the user is logged in
    const token = typeof window !== 'undefined' ? localStorage.getItem('noteworthy_token') : null;
    return {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {})
    };
};