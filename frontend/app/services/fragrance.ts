import { API_BASE_URL } from './apiConfig';
import { SmellSearchResponse, DescriptionResponse } from "../types/FragranceTypes";

export const fragranceService = {
    async searchBySmell(query: string, engine: string, limit: number = 20): Promise<SmellSearchResponse> {
        const encodedQuery = encodeURIComponent(query.trim());
        const response = await fetch(`${API_BASE_URL}/search/smell?query=${encodedQuery}&k=${limit}&engine=${engine}`);

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
    }
};