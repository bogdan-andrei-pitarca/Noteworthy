import React from 'react';
import { useState } from 'react';
import { ExternalLink, Sparkles } from 'lucide-react';
import { FragranceRecord } from '../types/FragranceTypes';
import { fragranceService } from '../services/api';

interface ResultCardProps {
    result: FragranceRecord;
}

const ResultCard: React.FC<ResultCardProps> = ({ result }) => {
    // local state for AI description
    const [aiDescription, setAiDescription] = useState<string | null>(null);
    const [isGenerating, setIsGenerating] = useState<boolean>(false);

    const scoreColor = result.similarity_percent > 80 ? 'bg-green-100 text-green-800' :
                       result.similarity_percent > 60 ? 'bg-yellow-100 text-yellow-800' :
                       'bg-red-100 text-red-800';

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
        try{
            const data = await fragranceService.generateDescription(result.all_notes);
            setAiDescription(data.description);
        } catch (error) {
            console.error("Error generating description:", error);
            setAiDescription("Sorry, an error occurred while generating the description.");
        } finally {
            setIsGenerating(false);
        }
    }

    return (
        <div className="bg-white p-5 rounded-xl shadow-lg border border-gray-100 hover:shadow-2xl transition duration-200 transform hover:scale-[1.02] flex flex-col justify-between">
            <div>
                <div className="flex justify-between items-start mb-3">
                    <h3 className="text-xl font-bold text-fuschia-800 capitalize leading-tight">
                        {(result.perfume_name || '').replace(/_/g, ' ')} by {result.brand} {result.launch_year ? `(${result.launch_year})` : ''}
                    </h3>
                    <a href={result.url} target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-fuschia-500 transition ml-2">
                        <ExternalLink className="w-4 h-4" />
                    </a>
                </div>
                <p className="text-sm text-gray-500 mb-2 font-semibold">{result.brand}</p>

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
                <span className={`px-4 py-1.5 text-sm font-bold rounded-full shadow-inner ${scoreColor}`}>
                    {result.similarity_percent}% Match
                </span>
                <span className="text-xs text-gray-500 italic">Gender: {result.gender}</span>
            </div>
        </div>
    )
}

export default ResultCard;