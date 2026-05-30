import { API_BASE_URL, getAuthHeaders } from "./apiConfig";
import { FragranceRecord } from "../types/FragranceTypes";

export const favoritesService = {
    async getFavorites(): Promise<FragranceRecord[]> {
        const response = await fetch(`${API_BASE_URL}/favorites/`, {
            method: 'GET',
            headers: getAuthHeaders()
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: 'Failed to fetch favorites' }));
            throw new Error(errorData.detail || `Error ${response.status}`);
        }
        return response.json();
    },

    async addFavorite(embedding_id: number) {
        const response = await fetch(`${API_BASE_URL}/favorites/${embedding_id}`, {
            method: 'POST',
            headers: getAuthHeaders()
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: 'Failed to add favorite' }));
            throw new Error(errorData.detail || `Error ${response.status}`);
        }
        return response.json();
    },

    async removeFavorite(embedding_id: number) {
        const response = await fetch(`${API_BASE_URL}/favorites/${embedding_id}`, {
            method: 'DELETE',
            headers: getAuthHeaders()
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: 'Failed to remove favorite' }));
            throw new Error(errorData.detail || `Error ${response.status}`);
        }
        return response.json();
    }
}