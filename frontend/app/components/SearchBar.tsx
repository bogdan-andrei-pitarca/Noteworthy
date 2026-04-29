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
        <div className="bg-white p-4 rounded-xl shadow-2xl border border-gray-100 w-full mb-6">
                {/* API Mode Selection */}
            <div className="flex items-center space-x-4 mb-4 border-b pb-3">
                <button
                    onClick= {() => setMode('notes_to_smell')}
                    className={`flex-1 p-3 rounded-lg transition duration-200 text-sm md:test-base flex items-center justify-center ${
                        mode === 'notes_to_smell'
                        ? 'bg-purple-600 text-white shadow-lg'
                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    }`}
                >
                    <Droplet className="w-4 h-4 mr-2" /> Notes to Description
                </button>
                <button
                    onClick= {() => setMode('smell_to_notes')}
                    className={`flex-1 p-3 rounded-lg transition duration-200 text-sm md:test-base flex items-center justify-center ${
                        mode === 'smell_to_notes'
                        ? 'bg-purple-600 text-white shadow-lg'
                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    }`}
                >
                    <Search className="w-4 h-4 mr-2" /> Description to Notes
                </button>
            </div>

            {/* Search Input*/}
            <div className="flex space-x-2">
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder={mode === 'notes_to_smell' ? 
                        'Enter fragrance notes (e.g., floral, woody, citrus)...' : 
                        'Describe the smell you are looking for...'}
                    className='flex-grow p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-gray-800'
                    onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                />
                <button
                    onClick={handleSearch}
                    className="bg-fuchsia-700 text-white p-3 rounded-lg hover:bg-fuchsia-800 transition duration-150 shadow-md flex items-center"
                >
                    <Zap className="w-5 h-5" /> Search
                </button>
            </div>

            {/* Engine Toggle */}
            {mode === 'smell_to_notes' && (
                <div className="flex items-center space-x-2 pt-2 border-t border-gray-50">
                    <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider flex items-center">
                        <Cpu className="w-3 h-3 mr-1"/> Engine:
                    </span>
                    {(['baseline', 'hybrid', 'sbert'] as SearchEngine[]).map((e) => (
                        <button
                            key={e}
                            onClick={() => setEngine(e)}
                            className={`px-3 py-1 text-xs rounded-full font-medium transition ${
                                engine === e 
                                ? 'bg-fuchsia-100 text-fuchsia-800 border border-fuchsia-300' 
                                : 'bg-gray-50 text-gray-500 hover:bg-gray-100 border border-gray-200'
                            }`}
                        >
                            {e === 'baseline' ? 'Base SBERT' : e === 'hybrid' ? 'Hybrid (Base+T5)' : 'Fine-Tuned SBERT'}
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
}

export default SearchBar;