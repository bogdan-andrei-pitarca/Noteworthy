import { useState, useCallback } from 'react';
import { fragranceService } from '../services/api';
import { SearchMode, FragranceRecord, DescriptionResponse } from '../types/FragranceTypes';

/**
 * Custom hook to manage fragrance search functionality.
 */

export function useFragranceSearch() {
    const [mode, setMode] = useState<SearchMode>('notes_to_smell');
    
    const [smellQuery, setSmellQuery] = useState<string>('');
    const [notesQuery, setNotesQuery] = useState<string>('');
    // We maintain separate state for each query type to preserve user input when switching modes

    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    const [searchMatches, setSearchMatches] = useState<FragranceRecord[]>([]);
    const [descriptionResult, setDescriptionResult] = useState<DescriptionResponse | null>(null);

    const performSearch = useCallback(async () => {

        // dynamically determine which query to use based on current mode
        const query = mode === 'notes_to_smell' ? notesQuery : smellQuery;

        if (!query.trim()) {
            setError('Please fill out the field before searching.');
            return;
        }

        setIsLoading(true);
        setError(null);
        setSearchMatches([]);
        setDescriptionResult(null);

        try {
            if (mode === 'notes_to_smell') {
                const data = await fragranceService.generateDescription(query);
                setDescriptionResult(data);
            } else {
                const data = await fragranceService.searchBySmell(query);
                if (data.results.length > 0) {
                    setSearchMatches(data.results);
                } else {
                    setError('No matching fragrances found. Try describing it differently!');
                }
            }
        } catch (err: any) {
            setError(err.message || 'An unexpected error occurred.');
        } finally {
            setIsLoading(false);
        }
    }, [mode, notesQuery, smellQuery]);

    return {
        mode,
        setMode,
        smellQuery,
        setSmellQuery,
        notesQuery,
        setNotesQuery,
        isLoading,
        error,
        searchMatches,
        descriptionResult,
        performSearch,
    }
}