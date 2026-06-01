import React from 'react';
import { useState } from 'react';
import { ExternalLink, Heart, Sparkles } from 'lucide-react';
import { FragranceRecord } from '../types/FragranceTypes';
import { fragranceService } from '../services';

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
                ? { text: "Perfect Match", color: "bg-fuchsia-100 text-fuchsia-800 border-fuchsia-200" }
                : { text: "Best Vibe Match", color: "bg-fuchsia-100 text-fuchsia-800 border-fuchsia-200" };
        }

        // The rest are graded on the calibrated curve
        if (percent >= 75) return { text: "Strong Match", color: "bg-green-100 text-green-800 border-green-200" };
        if (percent >= 50) return { text: "Good Match", color: "bg-blue-100 text-blue-800 border-blue-200" };
        if (percent >= 25) return { text: "Conceptual Match", color: "bg-indigo-100 text-indigo-800 border-indigo-200" };

        // Distant matches are neutral gray, not aggressive red
        return { text: "Distant Match", color: "bg-gray-100 text-gray-700 border-gray-200" };
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
        <div className="bg-white p-5 rounded-xl shadow-lg border border-gray-100 hover:shadow-2xl transition duration-200 transform hover:scale-[1.02] flex flex-col justify-between relative">

            {/* Grouped Actions Container in the Top Right */}
            <div className="absolute top-4 right-4 flex items-center gap-1">
                {/* External Link */}
                <a
                    href={result.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="p-2 text-gray-400 hover:text-fuchsia-500 transition rounded-full hover:bg-gray-50"
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
                                ? 'text-red-500 bg-red-50 hover:bg-red-100'
                                : 'text-gray-400 bg-gray-50 hover:text-red-500 hover:bg-gray-100'
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
                    <h3 className="text-xl font-bold text-fuchsia-800 capitalize leading-tight">
                        {(result.perfume_name || '').replace(/-/g, ' ')} by {(result.brand || '').replace(/-/g, ' ')} {result.launch_year ? `(${result.launch_year})` : ''}
                    </h3>
                </div>
                <p className="text-sm text-gray-500 mb-2 font-semibold">{(result.brand || '').replace(/-/g, ' ')}</p>

                <div className="flex flex-wrap gap-2 mb-3">
                    {accords.map(accord => (
                        <span key={accord} className="px-2 py-0.5 text-xs font-medium rounded-full bg-fuschia-50 text-fuschia-800 border border-fuschia-200 capitalize">
                            {accord}
                        </span>
                    ))}
                </div>

                <div className="text-xs text-gray-600 space-y-1">
                    <p><strong className="text-gray-700">Rating: {result.rating_value ?? 'N/A'} ({result.rating_count ?? '0'} reviews)</strong></p>
                    <p><strong className="text-gray-700">Launch Year: {result.launch_year ?? 'N/A'}</strong></p>
                </div>
            </div>

            <div className="mt-auto">
                {/* AI GENERATED DESCRIPTION SECTION */}
                <div className="bg-gray-50 p-3 rounded-lg border border-gray-100 mb-4 min-h-[80px] flex flex-col justify-center">
                    {aiDescription ? (
                        <div className="text-sm text-gray-700 italic font-serif leading-relaxed">
                            <Sparkles className="w-3 h-3 inline-block mr-1 text-fuschia-500 mb-1" />
                            "{aiDescription}"
                        </div>
                    ) : (
                        <button
                            onClick={handleGenerateDescription}
                            disabled={isGenerating}
                            className="w-full py-2 px-4 bg-fuchsia-100 text-fuchsia-700 text-sm font-semibold rounded-md hover:bg-fuchsia-200 transition disabled:opacity-50"
                        >
                            {isGenerating ? 'Generating...' : 'Find out how this smells!'}
                        </button>
                    )}
                </div>
            </div>

            <div className="mt-4 pt-4 border-t border-gray-100 flex justify-between items-center">
                {result.similarity_percent !== undefined && (
                    <span className={`px-4 py-1.5 text-sm font-bold rounded-full shadow-inner border ${badge.color}`}>
                        {badge.text}
                        {showScores && (
                            <span className="opacity-60 ml-1 font-normal text-xs">({result.similarity_percent}%)</span>
                        )}
                    </span>
                )}

                <span className="text-xs text-gray-500 italic">Gender: {result.gender}</span>
            </div>
        </div>
    )
}

export default ResultCard;