import React from 'react';
import { ExternalLink } from 'lucide-react';
import { FragranceRecord } from '../types/FragranceTypes';

interface ResultCardProps {
    result: FragranceRecord;
}

const ResultCard: React.FC<ResultCardProps> = ({ result }) => {
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