"use client";

import { useEffect, useState } from "react";
import { useAuth } from '../context/AuthContext';
import { favoritesService } from '../services';
import { FragranceRecord } from '../types/FragranceTypes';
import ResultCard from "../components/ResultCard";
import { RefreshCw, HeartCrack, LogIn } from "lucide-react";
import Link from "next/link";
import SkeletonCard from "../components/SkeletonCard";

export default function FavoritesPage() {
    const { isAuthenticated, isLoading: isAuthLoading } = useAuth();

    const [favorites, setFavorites] = useState<FragranceRecord[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // track the favorite IDs so the ResultCard can show the correct heart state
    const [favoriteIds, setFavoriteIds] = useState<Set<number>>(new Set());

    useEffect(() => {
        const fetchFavorites = async () => {
            if (!isAuthenticated) {
                setIsLoading(false);
                return;
            }

            try {
                const data = await favoritesService.getFavorites();
                setFavorites(data);
                setFavoriteIds(new Set(data.map(f => f.embedding_id)));
            } catch (err: any) {
                setError('Failed to load favorites. Please try again later.');
            } finally {
                setIsLoading(false);
            }
        }

        // only fetch if auth has finished loading
        if (!isAuthLoading) {
            fetchFavorites();
        }
    }, [isAuthenticated, isAuthLoading]);

    // handle removing a favorite directly from this page
    const handleToggleFavorite = async (embedding_id: number) => {
        try {
            await favoritesService.removeFavorite(embedding_id);
            // remove immediately from the UI
            setFavorites(prev => prev.filter(f => f.embedding_id !== embedding_id));
            setFavoriteIds(prev => {
                const newSet = new Set(prev);
                newSet.delete(embedding_id);
                return newSet;
            });
        } catch (err) {
            setError('Failed to remove favorite. Please try again.');
        }
    };

    // show loading state while AuthContext is determining if user is authenticated
    if (isAuthLoading || (isAuthenticated && isLoading)) {
        return (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {/* Render 6 fake cards while waiting for the API */}
                {[...Array(6)].map((_, i) => (
                    <SkeletonCard key={i} />
                ))}
            </div>
        );
    }

    // show not logged in state
    if (!isAuthenticated) {
        return (
            <div className="min-h-screen bg-gray-50 p-8 flex flex-col items-center justify-center text-center">
                <LogIn className="w-16 h-16 text-gray-300 mb-4" />
                <h2 className="text-2xl font-bold text-gray-800 mb-2">You aren't signed in</h2>
                <p className="text-gray-500 max-w-md mb-6">
                    Sign in to your account to view your personalized collection of saved fragrances.
                </p>
                <Link href="/">
                    <button className="bg-fuchsia-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-fuchsia-700 transition">
                        Go to Homepage
                    </button>
                </Link>
            </div>
        );
    }

    // show empty state (logged in but no favorites)
    if (favorites.length === 0 && !error) {
        return (
            <div className="min-h-screen bg-gray-50 p-8">
                <div className="max-w-6xl mx-auto">
                    <header className="border-b pb-6 mb-10">
                        <h1 className="text-3xl font-extrabold tracking-tight text-fuchsia-800">Your Collection</h1>
                    </header>
                    <div className="flex flex-col items-center justify-center py-20 text-center border-2 border-dashed border-gray-200 rounded-3xl bg-white">
                        <HeartCrack className="w-16 h-16 text-gray-300 mb-4" />
                        <h2 className="text-xl font-bold text-gray-800 mb-2">No favorites yet</h2>
                        <p className="text-gray-500 max-w-md mb-6">
                            You haven't saved any fragrances to your collection. Head back to the search page to explore!
                        </p>
                        <Link href="/">
                            <button className="bg-fuchsia-100 text-fuchsia-700 border border-fuchsia-200 px-6 py-2 rounded-lg font-semibold hover:bg-fuchsia-200 transition">
                                Discover Fragrances
                            </button>
                        </Link>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 p-8">
            <div className="max-w-6xl mx-auto">
                <header className="border-b pb-6 mb-8 flex justify-between items-end">
                    <div>
                        <h1 className="text-3xl font-extrabold tracking-tight text-fuchsia-800 mb-2">Your Collection</h1>
                        <p className="text-gray-600">You have saved {favorites.length} {favorites.length === 1 ? 'fragrance' : 'fragrances'}.</p>
                    </div>
                    <Link href="/">
                        <button className="text-sm font-semibold text-fuchsia-600 hover:text-fuchsia-800 hover:underline">
                            &larr; Back to Search
                        </button>
                    </Link>
                </header>

                {error && (
                    <div className="p-4 mb-8 bg-red-50 text-red-700 rounded-lg border border-red-200">
                        {error}
                    </div>
                )}

                <div className="grid text-gray-800 grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {favorites.map((fragrance, index) => (
                        <ResultCard 
                            key={fragrance.embedding_id} 
                            result={fragrance} 
                            index={index} 
                            showScores={false} // Hide scores on favorites page since they weren't searched for here
                            isAuthenticated={true}
                            isFavorite={favoriteIds.has(fragrance.embedding_id)}
                            onToggleFavorite={handleToggleFavorite}
                        />
                    ))}
                </div>
            </div>
        </div>
    );
}