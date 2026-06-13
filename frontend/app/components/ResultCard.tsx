import React from 'react';
import { useState } from 'react';
import { ExternalLink, Heart, Sparkles } from 'lucide-react';
import { FragranceRecord } from '../types/FragranceTypes';
import { fragranceService } from '../services';
import Link from 'next/link';

interface ResultCardProps {
    result: FragranceRecord;
    index: number;
    showScores?: boolean; // optional prop to toggle score display 
    isFavorite?: boolean; // optional prop to indicate if this is in the favorites list
    onToggleFavorite?: (id: number) => void; // callback for toggling favorite status
    isAuthenticated?: boolean; // to conditionally show favorite button
}

const ResultCard: React.FC<ResultCardProps> = ({
    result,
    index,
    showScores = false,
    isFavorite = false,
    onToggleFavorite,
    isAuthenticated = false
}) => {
    // local state for AI description
    const [aiDescription, setAiDescription] = useState<string | null>(null);
    const [isGenerating, setIsGenerating] = useState<boolean>(false);
    const [isHeartLoading, setIsHeartLoading] = useState(false);

    const getBadgeInfo = (percent: number | undefined, rank: number) => {
        if (percent === undefined) {
            return { text: "", color: "" };
        }

        // Rank 1 gets special treatment regardless of raw score
        if (rank === 0) {
            return percent > 50
                ? { text: "Perfect Match", color: "bg-fuchsia-500/20 text-fuchsia-300 border-fuchsia-500/30" }
                : { text: "Best Vibe Match", color: "bg-fuchsia-500/20 text-fuchsia-300 border-fuchsia-500/30" };
        }

        // The rest are graded on the calibrated curve
        if (percent >= 75) return { text: "Strong Match", color: "bg-green-500/15 text-green-400 border-green-500/30" };
        if (percent >= 50) return { text: "Good Match", color: "bg-blue-500/15 text-blue-400 border-blue-500/30" };
        if (percent >= 25) return { text: "Conceptual Match", color: "bg-indigo-500/15 text-indigo-400 border-indigo-500/30" };

        // Distant matches are neutral gray, not aggressive red
        return { text: "Distant Match", color: "bg-zinc-800 text-zinc-400 border-zinc-700" };
    };

    const badge = getBadgeInfo(result.similarity_percent, index);

    const accords = [
        result.main_accord_1,
        result.main_accord_2,
        result.main_accord_3,
        result.main_accord_4,
        result.main_accord_5
    ].filter(accord => accord && accord.toLowerCase() !== 'none');


    // calls backend T5 API
    const handleGenerateDescription = async () => {
        setIsGenerating(true);
        try {
            const data = await fragranceService.generateDescription(result.all_notes);
            setAiDescription(data.description);
        } catch (error) {
            console.error("Error generating description:", error);
            setAiDescription("Sorry, an error occurred while generating the description.");
        } finally {
            setIsGenerating(false);
        }
    }

    const handleHeartClick = async () => {
        if (!onToggleFavorite || !isAuthenticated) return;

        setIsHeartLoading(true);
        try {
            await onToggleFavorite(result.embedding_id);
        } catch (error) {
            console.error("Error toggling favorite:", error);
        } finally {
            setIsHeartLoading(false);
        }
    }

    return (
        <div className="bg-zinc-900/70 backdrop-blur-sm p-6 rounded-2xl border border-zinc-800 border-l-4 border-l-fuchsia-500 hover:border-zinc-700 hover:shadow-xl hover:shadow-fuchsia-500/10 transition-all duration-300 transform hover:-translate-y-1 flex flex-col justify-between relative">

            {/* Grouped Actions Container in the Top Right */}
            <div className="absolute top-4 right-4 flex items-center gap-1">
                {/* External Link */}
                <a
                    href={result.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="p-2 text-zinc-400 hover:text-fuchsia-500 transition rounded-full hover:bg-zinc-800"
                    title="View on Fragrantica"
                >
                    <ExternalLink className="w-4 h-4" />
                </a>

                {/* Favorite Button (Only show if authenticated) */}
                {isAuthenticated && (
                    <button
                        onClick={handleHeartClick}
                        disabled={isHeartLoading}
                        className={`p-2 rounded-full transition-colors ${isFavorite
                            ? 'text-red-500 bg-red-500/15 hover:bg-red-500/25'
                            : 'text-zinc-400 bg-zinc-800 hover:text-red-500 hover:bg-zinc-700'
                            } ${isHeartLoading ? 'opacity-50 cursor-wait' : ''}`}
                        title={isFavorite ? "Remove from favorites" : "Add to favorites"}
                    >
                        <Heart className="w-5 h-5" fill={isFavorite ? "currentColor" : "none"} />
                    </button>
                )}
            </div>

            <div>
                {/* pr-24 ensures text wraps before hitting the icon group */}
                <div className="flex justify-between items-start mb-3 pr-24">
                    <Link href={`/fragrance/${result.embedding_id}`}>
                        <h3 className="text-xl font-bold text-fuchsia-400 capitalize leading-tight hover:underline cursor-pointer">
                            {(result.perfume_name || '').replace(/-/g, ' ')} by {(result.brand || '').replace(/-/g, ' ')} {result.launch_year ? `(${result.launch_year})` : ''}
                        </h3>
                    </Link>
                </div>
                <p className="text-sm text-zinc-400 mb-2 font-semibold">{(result.brand || '').replace(/-/g, ' ')}</p>

                <div className="flex flex-wrap gap-2 mb-3">
                    {accords.map(accord => (
                        <span key={accord} className="px-2.5 py-1 text-[11px] font-semibold tracking-wide rounded-md bg-zinc-800 text-zinc-300 border border-zinc-700 uppercase">
                            {accord}
                        </span>
                    ))}
                </div>

                <div className="text-xs text-zinc-400 space-y-1">
                    <p><strong className="text-zinc-300">Rating: {result.rating_value ?? 'N/A'} ({result.rating_count ?? '0'} reviews)</strong></p>
                    <p><strong className="text-zinc-300">Launch Year: {result.launch_year ?? 'N/A'}</strong></p>
                </div>
            </div>

            <div className="mt-auto">
                {/* AI GENERATED DESCRIPTION SECTION */}
                <div className="bg-zinc-800/50 p-3 rounded-lg border border-zinc-700 mb-4 min-h-[80px] flex flex-col justify-center">
                    {aiDescription ? (
                        <div className="text-sm text-zinc-300 italic font-serif leading-relaxed">
                            <Sparkles className="w-3 h-3 inline-block mr-1 text-fuchsia-500 mb-1" />
                            "{aiDescription}"
                        </div>
                    ) : (
                        <button
                            onClick={handleGenerateDescription}
                            disabled={isGenerating}
                            className="w-full py-2 px-4 bg-fuchsia-500/20 text-fuchsia-300 text-sm font-semibold rounded-md hover:bg-fuchsia-500/30 transition disabled:opacity-50"
                        >
                            {isGenerating ? 'Generating...' : 'Find out how this smells!'}
                        </button>
                    )}
                </div>
            </div>

            <div className="mt-4 pt-4 border-t border-zinc-800 flex justify-between items-center">
                {result.similarity_percent !== undefined && (
                    <span className={`px-4 py-1.5 text-sm font-bold rounded-full shadow-inner border ${badge.color}`}>
                        {badge.text}
                        {showScores && (
                            <span className="opacity-60 ml-1 font-normal text-xs">({result.similarity_percent}%)</span>
                        )}
                    </span>
                )}

                <span className="text-xs text-zinc-500 italic">Gender: {result.gender}</span>
            </div>
        </div>
    )
}

export default ResultCard;