"use client";

import { useState } from "react";
import { RefreshCw, Sparkles } from "lucide-react";
import { useFragranceSearch } from "./hooks/useFragranceSearch";
import ResultCard from "./components/ResultCard";
import SearchBar from "./components/SearchBar";
import { useAuth } from "./context/AuthContext";
import SkeletonCard from "./components/SkeletonCard";

export default function AIModelInterface() {
  const { isAuthenticated } = useAuth();

  const {
    mode,
    setMode,
    engine,
    setEngine,
    smellQuery,
    setSmellQuery,
    notesQuery,
    setNotesQuery,
    isLoading,
    searchMatches,
    descriptionResult,
    performSearch,
    showScores,
    setShowScores,
    favoriteIds,
    toggleFavorite,
    currentPage,
    totalPages
  } = useFragranceSearch();

  // determine active query based on mode
  const activeQuery = mode === 'notes_to_smell' ? notesQuery : smellQuery;
  const setActiveQuery = mode === 'notes_to_smell' ? setNotesQuery : setSmellQuery;

  return (
    <div className="min-h-screen bg-gray-50 p-8 font-sans text-gray-800">
      <div className="max-w-6xl mx-auto bg-white p-6 rounded-xl shadow-lg space-y-8">

        { /* Header Section */}
        <header className="text-center border-b pb-6">
          <h1 className="text-3xl font-extrabold tracking-tight text-fuchsia-800 mb-2">Noteworthy AI</h1>
          <p className="text-gray-600 text-lg mt-2">Bimodal pipeline using SBERT for retrieval and T5 for generation.</p>
        </header>

        <div className="max-w-3xl mx-auto">
          <SearchBar
            mode={mode}
            setMode={setMode}
            engine={engine}
            setEngine={setEngine}
            query={activeQuery}
            setQuery={setActiveQuery}
            handleSearch={() => performSearch(1)}
          />
        </div>

        { /* RESULTS SECTION */}
        <div className="mt-8">
          {isLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {Array.from({ length: 6 }).map((_, index) => (
                <SkeletonCard key={index} />
              ))}
            </div>
          ) : (
            <div className="space-y-10">
              {/* T5 OUTPUT (DESCRIPTION) */}
              {descriptionResult && (
                <div className="max-w-3xl mx-auto bg-gradient-to-br from-green-50 to-white p-8 rounded-2xl border border-green-100 shadow-sm">
                  <div className="flex items-center gap-2 mb-4 text-green-700 font-bold uppercase tracking-widest text-xs">
                    <Sparkles size={18} /> Description
                  </div>
                  <p className="text-2xl text-gray-800 italic font-serif loading-relaxed"> "{descriptionResult.description}" </p>
                </div>
              )}

              {/* SBERT OUTPUT (THE MARKETPLACE GRID) */}
              {searchMatches.length > 0 && (
                <>
                  <div className="flex justify-end pr-1">
                    <button
                      onClick={() => setShowScores(s => !s)}
                      className="text-xs text-gray-500 hover:text-fuchsia-700 flex items-center gap-1.5 transition"
                    >
                      <span className={`w-8 h-4 rounded-full transition-colors duration-200 flex items-center px-0.5 ${showScores ? 'bg-fuchsia-500' : 'bg-gray-300'}`}>
                        <span className={`w-3 h-3 bg-white rounded-full shadow transition-transform duration-200 ${showScores ? 'translate-x-4' : 'translate-x-0'}`} />
                      </span>
                      Similarity scores
                    </button>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {searchMatches.map((match, index) => (
                      <ResultCard
                        key={match.embedding_id}
                        result={match}
                        index={index}
                        showScores={showScores}
                        isAuthenticated={isAuthenticated}
                        isFavorite={favoriteIds.has(match.embedding_id)}
                        onToggleFavorite={toggleFavorite}
                      />
                    ))}
                  </div>

                  {totalPages > 1 && (
                    <div className="flex items-center justify-center space-x-6 mt-12 pt-8 border-t border-gray-100">
                      <button
                        onClick={() => performSearch(currentPage - 1)}
                        disabled={currentPage === 1 || isLoading}
                        className="px-5 py-2 rounded-lg font-semibold text-sm transition-colors disabled:opacity-40 disabled:cursor-not-allowed bg-white border border-gray-200 text-gray-700 hover:bg-gray-50 hover:text-fuchsia-600"
                      >
                        &larr; Previous
                      </button>
                      <span className="text-sm font-medium text-gray-500">
                        Page <strong className="text-gray-900">{currentPage}</strong> of <strong className="text-gray-900">{totalPages}</strong>
                      </span>
                      <button
                        onClick={() => performSearch(currentPage + 1)}
                        disabled={currentPage === totalPages || isLoading}
                        className="px-5 py-2 rounded-lg font-semibold text-sm transition-colors disabled:opacity-40 disabled:cursor-not-allowed bg-white border border-gray-200 text-gray-700 hover:bg-gray-50 hover:text-fuchsia-600"
                      >
                        Next &rarr;
                      </button>
                    </div>
                  )}
                </>
              )}

              {/* NO RESULTS */}
              {!searchMatches.length && !descriptionResult && (
                <div className="text-center py-20 border-2 border-dashed border-gray-200 rounded-3xl">
                  <p className="text-gray-400 italic">Enter a fragrance or description and begin your search!</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}