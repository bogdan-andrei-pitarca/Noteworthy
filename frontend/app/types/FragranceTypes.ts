/**
 * All the required types for the fragrance application.
 */

export interface FragranceRecord {
    embedding_id: number;
    perfume_name: string;
    brand: string;
    gender: string;
    launch_year: number | null;
    rating_value: number | null;
    rating_count: number | null;
    url: string;
    main_accord_1: string;
    main_accord_2: string;
    main_accord_3: string;
    main_accord_4: string;
    main_accord_5: string;
    all_notes: string;
    similarity_percent?: number;
}

export interface SmellSearchResponse{
    query: string;
    results: FragranceRecord[];
}

export interface DescriptionResponse{
    query_notes: string[];
    description: string;
    model_status: string;
}

export type SearchMode = 'notes_to_smell' | 'smell_to_notes';
export type SearchEngine = 'baseline' | 'hybrid' | 'sbert';