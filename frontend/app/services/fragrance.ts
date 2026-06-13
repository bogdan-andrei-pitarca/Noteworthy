import { API_BASE_URL } from './apiConfig';
import { SmellSearchResponse, DescriptionResponse, FragranceRecord } from "../types/FragranceTypes";

export const fragranceService = {
    async searchBySmell(query: string, engine: string, page: number = 1, limit: number = 12): Promise<SmellSearchResponse> {
        const encodedQuery = encodeURIComponent(query.trim());
        const response = await fetch(`${API_BASE_URL}/search/smell?query=${encodedQuery}&engine=${engine}&page=${page}&page_size=${limit}`);

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: 'Backend error occurred' }));
            throw new Error(errorData.detail || `Error ${response.status}`);
        }
        return response.json();
    },

    async generateDescription(notes: string): Promise<DescriptionResponse> {
        const encodedNotes = encodeURIComponent(notes.trim());
        const response = await fetch(`${API_BASE_URL}/search/notes_to_description?notes=${encodedNotes}`);

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: 'Backend error occurred' }));
            throw new Error(errorData.detail || `Error ${response.status}`);
        }
        return response.json();
    },

    async getFragranceById(id: number): Promise<FragranceRecord> {
        const response = await fetch(`${API_BASE_URL}/search/details/${id}`);
        if (!response.ok) {
            throw new Error(`Error fetching fragrance details: ${response.statusText}`);
        }
        return response.json();
    },

    async getSimilarFragrances(id: number, engine: string = 'sbert'): Promise<FragranceRecord[]> {
        const response = await fetch(`${API_BASE_URL}/search/similar/${id}?engine=${engine}`);
        if (!response.ok) {
            throw new Error(`Error fetching similar fragrances: ${response.statusText}`);
        }
        return response.json();
    },

    async getScentProfile(favoriteIds: number[]): Promise<any[]> {
        const response = await fetch(`${API_BASE_URL}/search/profile/radar`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ favorite_ids: favoriteIds })
        });
        if (!response.ok) {
            throw new Error(`Error fetching scent profile: ${response.statusText}`);
        }
        return response.json();
    }
};