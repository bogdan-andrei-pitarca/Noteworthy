"use client";

import { useEffect, useState } from "react";
import { useAuth } from '../context/AuthContext';
import { favoritesService } from '../services';
import { FragranceRecord } from '../types/FragranceTypes';
import ResultCard from "../components/ResultCard";
import { RefreshCw, HeartCrack, LogIn } from "lucide-react";
import Link from "next/link";
import SkeletonCard from "../components/SkeletonCard";
import toast from "react-hot-toast";

export default function FavoritesPage() {
    const { isAuthenticated, isLoading: isAuthLoading } = useAuth();

    const [favorites, setFavorites] = useState<FragranceRecord[]>([]);
    const [isLoading, setIsLoading] = useState(true);

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
                toast.error('Failed to load favorites. Please try again later.');
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
            toast.error('Failed to remove favorite. Please try again.');
        }
    };

    // show loading state while AuthContext is determining if user is authenticated
    if (isAuthLoading || (isAuthenticated && isLoading)) {
        return (
            <div className="min-h-screen bg-zinc-950 p-8">
                <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {/* Render 6 fake cards while waiting for the API */}
                    {[...Array(6)].map((_, i) => (
                        <SkeletonCard key={i} />
                    ))}
                </div>
            </div>
        );
    }

    // show not logged in state
    if (!isAuthenticated) {
        return (
            <div className="min-h-screen bg-zinc-950 p-8 flex flex-col items-center justify-center text-center">
                <LogIn className="w-16 h-16 text-zinc-600 mb-4" />
                <h2 className="text-2xl font-bold text-zinc-200 mb-2">You aren't signed in</h2>
                <p className="text-zinc-400 max-w-md mb-6">
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
    if (favorites.length === 0) {
        return (
            <div className="min-h-screen bg-zinc-950 p-8">
                <div className="max-w-6xl mx-auto">
                    <header className="border-b border-zinc-800 pb-6 mb-10">
                        <h1 className="text-3xl font-extrabold tracking-tight text-fuchsia-400">Your Collection</h1>
                    </header>
                    <div className="flex flex-col items-center justify-center py-20 text-center border-2 border-dashed border-zinc-800 rounded-3xl bg-zinc-900/50">
                        <HeartCrack className="w-16 h-16 text-zinc-600 mb-4" />
                        <h2 className="text-xl font-bold text-zinc-200 mb-2">No favorites yet</h2>
                        <p className="text-zinc-400 max-w-md mb-6">
                            You haven't saved any fragrances to your collection. Head back to the search page to explore!
                        </p>
                        <Link href="/">
                            <button className="bg-fuchsia-500/20 text-fuchsia-300 border border-fuchsia-500/30 px-6 py-2 rounded-lg font-semibold hover:bg-fuchsia-500/30 transition">
                                Discover Fragrances
                            </button>
                        </Link>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-zinc-950 p-8">
            <div className="max-w-6xl mx-auto">
                <header className="border-b border-zinc-800 pb-6 mb-8 flex justify-between items-end">
                    <div>
                        <h1 className="text-3xl font-extrabold tracking-tight text-fuchsia-400 mb-2">Your Collection</h1>
                        <p className="text-zinc-400">You have saved {favorites.length} {favorites.length === 1 ? 'fragrance' : 'fragrances'}.</p>
                    </div>
                    <Link href="/">
                        <button className="text-sm font-semibold text-fuchsia-600 hover:text-fuchsia-400 hover:underline">
                            &larr; Back to Search
                        </button>
                    </Link>
                </header>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
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