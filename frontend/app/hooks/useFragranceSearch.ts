import { useState, useCallback, useEffect } from 'react';
import { fragranceService, favoritesService } from '../services';
import { SearchMode, SearchEngine, FragranceRecord, DescriptionResponse } from '../types/FragranceTypes';
import { useAuth } from '../context/AuthContext';

/**
 * Custom hook to manage fragrance search functionality.
 */

export function useFragranceSearch() {
    const { isAuthenticated } = useAuth();

    const [mode, setMode] = useState<SearchMode>('notes_to_smell');
    const [engine, setEngine] = useState<SearchEngine>('sbert'); // default search engine
    
    const [smellQuery, setSmellQuery] = useState<string>('');
    const [notesQuery, setNotesQuery] = useState<string>('');
    // We maintain separate state for each query type to preserve user input when switching modes

    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    const [searchMatches, setSearchMatches] = useState<FragranceRecord[]>([]);
    const [descriptionResult, setDescriptionResult] = useState<DescriptionResponse | null>(null);

    const [showScores, setShowScores] = useState(false);

    const [favoriteIds, setFavoriteIds] = useState<Set<number>>(new Set());

    useEffect(() => {
        const fetchFavorites = async () => {
            if (isAuthenticated) {
                try {
                    const favorites = await favoritesService.getFavorites();
                    const ids = new Set(favorites.map(f => f.embedding_id));
                    setFavoriteIds(ids);
                } catch (err) {
                    console.error("Failed to fetch favorites:", err);
                }
            } else {
                setFavoriteIds(new Set()); // clear if logged out
            }
        };

        fetchFavorites();
    }, [isAuthenticated]);

    const toggleFavorite = async (embedding_id: number) => {
        if (!isAuthenticated) return;

        const isFavorited = favoriteIds.has(embedding_id);

        try {
            if (isFavorited) {
                await favoritesService.removeFavorite(embedding_id);
                setFavoriteIds(prev => {
                    const newSet = new Set(prev);
                    newSet.delete(embedding_id);
                    return newSet;
                });
            } else {
                await favoritesService.addFavorite(embedding_id);
                setFavoriteIds(prev => {
                    const newSet = new Set(prev);
                    newSet.add(embedding_id);
                    return newSet;
                });
            }
        } catch (err) {
            console.error("Failed to update favorite:", err);
        }
    }

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
                const data = await fragranceService.searchBySmell(query, engine);
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
    }, [mode, engine, notesQuery, smellQuery]);

    return {
        mode,
        setMode,
        engine,
        setEngine,
        smellQuery,
        setSmellQuery,
        notesQuery,
        setNotesQuery,
        isLoading,
        error,
        searchMatches,
        descriptionResult,
        performSearch,
        showScores,
        setShowScores,
        favoriteIds,
        toggleFavorite
    }
}