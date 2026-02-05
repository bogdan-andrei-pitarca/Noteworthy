import { SmellSearchResponse, DescriptionResponse } from "../types/FragranceTypes";
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export const fragranceService = {
    async searchBySmell(query: string, limit: number = 20): Promise<SmellSearchResponse> {
        const encodedQuery = encodeURIComponent(query.trim());
        const response = await fetch(`${API_BASE_URL}/search_by_smell?query=${encodedQuery}&limit=${limit}`);

        if (!response.ok) {
            const errorData = await response.json().catch(
                () => ({ detail: 'Backend error occurred' })
            )
            throw new Error(errorData.detail || `Error ${response.status}`);
        }

        return response.json();
    },

    async generateDescription(notes: string): Promise<DescriptionResponse> {
        const encodedNotes = encodeURIComponent(notes.trim());
        const response = await fetch(`${API_BASE_URL}/search/notes_to_description?notes=${encodedNotes}`);

        if (!response.ok) {
            const errorData = await response.json().catch(
                () => ({ detail: 'Backend error occurred' })
            );

            throw new Error(errorData.detail || `Error ${response.status}`);
        }

        return response.json();
    }
}