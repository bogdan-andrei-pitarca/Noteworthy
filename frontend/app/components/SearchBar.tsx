import React from 'react';
import { Search, Zap, Droplet, Cpu } from 'lucide-react';
import { SearchMode, SearchEngine } from '../types/FragranceTypes';

interface SearchBarProps {
    mode: SearchMode;
    setMode: (mode: SearchMode) => void;
    engine: SearchEngine;
    setEngine: (engine: SearchEngine) => void;
    query: string;
    setQuery: (query: string) => void;
    handleSearch: () => void;
}

export const SearchBar: React.FC<SearchBarProps> = ({ 
    mode, setMode, engine, setEngine, query, setQuery, handleSearch 
}) => {
    return (
        <div className="bg-white p-5 rounded-2xl shadow-xl shadow-fuchsia-900/5 border border-gray-100 w-full mb-6">
                {/* API Mode Selection */}
            <div className="flex items-center space-x-3 mb-5 border-b border-gray-100 pb-5">
                <button
                    onClick= {() => setMode('notes_to_smell')}
                    className={`flex-1 p-3.5 rounded-xl transition-all duration-200 text-sm md:test-base font-semibold flex items-center justify-center ${
                        mode === 'notes_to_smell'
                        ? 'bg-gradient-to-r from-fuchsia-600 to-fuchsia-500 text-white shadow-md shadow-fuchsia-500/20'
                        : 'bg-gray-50 text-gray-500 hover:bg-gray-100 hover:text-gray-800 border border-gray-200/60'
                    }`}
                >
                    <Droplet className="w-5 h-5 mr-2" /> Notes to Description
                </button>
                <button
                    onClick= {() => setMode('smell_to_notes')}
                    className={`flex-1 p-3.5 rounded-xl transition-all duration-200 text-sm md:test-base font-semibold flex items-center justify-center ${
                        mode === 'smell_to_notes'
                        ? 'bg-gradient-to-r from-fuchsia-600 to-fuchsia-500 text-white shadow-md shadow-fuchsia-500/20'
                        : 'bg-gray-50 text-gray-500 hover:bg-gray-100 hover:text-gray-800 border border-gray-200/60'
                    }`}
                >
                    <Search className="w-5 h-5 mr-2" /> Description to Notes
                </button>
            </div>

            {/* Search Input*/}
            <div className="flex flex-col md:flex-row gap-3">
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder={mode === 'notes_to_smell' ? 
                        'Enter fragrance notes (e.g., floral, woody, citrus)...' : 
                        'Describe the smell you are looking for...'}
                    className='flex-grow p-4 bg-gray-50/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-fuchsia-500/50 focus:border-fuchsia-500 text-gray-800 transition-all text-base placeholder:text-gray-400'
                    onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                />
                <button
                    onClick={handleSearch}
                    className="bg-gray-900 text-white px-8 py-4 rounded-xl hover:bg-gray-800 transition-all duration-200 shadow-md flex items-center justify-center font-bold text-base whitespace-nowrap"
                >
                    <Zap className="w-5 h-5 mr-2 text-fuchsia-400" /> Search
                </button>
            </div>

            {/* Engine Toggle */}
            {mode === 'smell_to_notes' && (
                <div className="flex flex-col sm:flex-row sm:items-center gap-3 pt-5 mt-4 border-t border-gray-50">
                    <span className="text-xs font-bold text-gray-400 uppercase tracking-wider flex items-center">
                        <Cpu className="w-4 h-4 mr-1.5"/> Engine:
                    </span>
                    <div className="flex flex-wrap gap-2">
                        {(['baseline', 'hybrid', 'sbert'] as SearchEngine[]).map((e) => (
                            <button
                                key={e}
                                onClick={() => setEngine(e)}
                                className={`px-4 py-2 text-xs rounded-lg font-semibold transition-all ${
                                    engine === e 
                                    ? 'bg-fuchsia-50 text-fuchsia-700 border border-fuchsia-200 shadow-sm' 
                                    : 'bg-white text-gray-500 hover:bg-gray-50 hover:text-gray-700 border border-gray-200'
                                }`}
                            >
                                {e === 'baseline' ? 'Base SBERT' : e === 'hybrid' ? 'Hybrid (Base+T5)' : 'Fine-Tuned SBERT'}
                            </button>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}

export default SearchBar;