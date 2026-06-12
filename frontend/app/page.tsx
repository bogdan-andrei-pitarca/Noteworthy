"use client";

import { useState, useEffect } from "react";
import { RefreshCw, Search, Sparkles } from "lucide-react";
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

  // typewriter effect for the hero subtitle
  const searchExamples = [
    "old dusty library books...",
    "warm cashmere by a fireplace...",
    "smoky leather and dark rum...",
    "fresh rain on concrete..."
  ];
  const [exampleIndex, setExampleIndex] = useState(0);
  const [displayText, setDisplayText] = useState("");
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    const currentWord = searchExamples[exampleIndex];
    const timeout = setTimeout(() => {
      if (!isDeleting) {
        setDisplayText(currentWord.substring(0, displayText.length + 1));
        if (displayText === currentWord) {
          setTimeout(() => setIsDeleting(true), 2000); // Pause at end of word
        }
      } else {
        setDisplayText(currentWord.substring(0, displayText.length - 1));
        if (displayText === "") {
          setIsDeleting(false);
          setExampleIndex((prev) => (prev + 1) % searchExamples.length);
        }
      }
    }, isDeleting ? 40 : 100); // Typing speed vs deleting speed

    return () => clearTimeout(timeout);
  }, [displayText, isDeleting, exampleIndex]);

  return (
    <div className="min-h-screen bg-gray-50 font-sans text-gray-800 pb-20">

      {/* 1. Hero Section (Dark with Radial Gradient) */}
      <div
        className="relative w-full pt-24 pb-32 px-6 overflow-hidden"
        style={{
          background: "radial-gradient(ellipse at 50% 0%, #2d0a3e 0%, #0a0a0f 70%)"
        }}
      >
        <div className="relative z-10 max-w-6xl mx-auto text-center">
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-white mb-4">
            Noteworthy <span className="text-transparent bg-clip-text bg-gradient-to-r from-fuchsia-400 to-pink-500">AI</span>
          </h1>
          <div className="h-8 mt-4">
            <p className="text-zinc-400 text-lg md:text-xl font-medium">
              Find fragrances that smell like <span className="text-fuchsia-400">"{displayText}"</span>
              <span className="animate-pulse text-fuchsia-400">|</span>
            </p>
          </div>
        </div>
      </div>

      {/* 2. Main Content Area (Overlapping the Hero) */}
      <div className="max-w-6xl mx-auto px-6 -mt-16 relative z-20 space-y-8">

        {/* Search Bar Container */}
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

        { /* 3. RESULTS SECTION (Light Theme) */}
        <div className="mt-8 pt-4">
          {isLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {Array.from({ length: 6 }).map((_, index) => (
                <SkeletonCard key={index} />
              ))}
            </div>
          ) : (
            <div className="space-y-10">
              {/* T5 OUTPUT (DESCRIPTION) */}
              {mode === 'notes_to_smell' && descriptionResult && (
                <div className="max-w-3xl mx-auto bg-gradient-to-br from-fuchsia-50 to-white p-8 rounded-2xl border border-fuchsia-100 shadow-sm">
                  <div className="flex items-center gap-2 mb-4 text-fuchsia-700 font-bold uppercase tracking-widest text-xs">
                    <Sparkles size={18} /> Description
                  </div>
                  <p className="text-2xl text-gray-800 italic font-serif leading-relaxed"> "{descriptionResult.description}" </p>
                </div>
              )}

              {/* SBERT OUTPUT (THE MARKETPLACE GRID) */}
              {mode === 'smell_to_notes' && searchMatches.length > 0 && (
                <>
                  <div className="flex justify-between items-end mb-6">
                    <h2 className="text-2xl font-extrabold text-gray-900 tracking-tight">Results</h2>
                    <button
                      onClick={() => setShowScores(s => !s)}
                      className="text-xs font-semibold text-gray-600 hover:text-fuchsia-700 flex items-center gap-2 transition px-3 py-1.5 rounded-full bg-white border border-gray-200 shadow-sm hover:border-fuchsia-200 hover:shadow-md"
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
                    <div className="flex items-center justify-center space-x-6 mt-12 pt-8 border-t border-gray-200">
                      <button
                        onClick={() => performSearch(currentPage - 1)}
                        disabled={currentPage === 1 || isLoading}
                        className="px-5 py-2 rounded-xl font-semibold text-sm transition-all disabled:opacity-40 disabled:cursor-not-allowed bg-white border border-gray-200 text-gray-700 hover:bg-gray-50 hover:text-fuchsia-600 hover:border-fuchsia-200 shadow-sm"
                      >
                        &larr; Previous
                      </button>
                      <span className="text-sm font-medium text-gray-500 bg-white px-4 py-1.5 rounded-full border border-gray-200 shadow-sm">
                        Page <strong className="text-gray-900">{currentPage}</strong> of <strong className="text-gray-900">{totalPages}</strong>
                      </span>
                      <button
                        onClick={() => performSearch(currentPage + 1)}
                        disabled={currentPage === totalPages || isLoading}
                        className="px-5 py-2 rounded-xl font-semibold text-sm transition-all disabled:opacity-40 disabled:cursor-not-allowed bg-white border border-gray-200 text-gray-700 hover:bg-gray-50 hover:text-fuchsia-600 hover:border-fuchsia-200 shadow-sm"
                      >
                        Next &rarr;
                      </button>
                    </div>
                  )}
                </>
              )}

              {/* NO RESULTS */}
              {((mode === 'notes_to_smell' && !descriptionResult) || 
                (mode === 'smell_to_notes' && searchMatches.length === 0)) && (
                <div className="text-center py-24 border-2 border-dashed border-gray-200 rounded-3xl bg-white shadow-sm">
                  <div className="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Search className="w-8 h-8 text-gray-300" />
                  </div>
                  <h3 className="text-lg font-bold text-gray-700 mb-1">Ready to explore</h3>
                  <p className="text-gray-500 max-w-md mx-auto">Enter fragrance notes or describe a scent to begin searching the catalog.</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}