import React from 'react';
import { Search, Zap, Droplet } from 'lucide-react';
import { SearchMode } from '../types/FragranceTypes';

interface SearchBarProps {
    mode: SearchMode;
    setMode: (mode: SearchMode) => void;
    query: string;
    setQuery: (query: string) => void;
    handleSearch: () => void;
}

export const SearchBar: React.FC<SearchBarProps> = ({ 
    mode, setMode, query, setQuery, handleSearch 
}) => {
    return (
        <div className="bg-white p-4 rounded-xl shadow-2xl border border-gray-100 w-full mb-6">
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
                    <Search className="w-4 h-4 mr-2" /> Smell to Notes
                </button>
            </div>

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
        </div>
    );
}

export default SearchBar;