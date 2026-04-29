"use client";

import { useState } from "react";
import { RefreshCw, Sparkles } from "lucide-react";
import { useFragranceSearch } from "./hooks/useFragranceSearch";
import ResultCard from "./components/ResultCard";
import SearchBar from "./components/SearchBar";

export default function AIModelInterface() {
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
    error,
    searchMatches,
    descriptionResult,
    performSearch,
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
          <p className="text-gray-600 text-lg mt-2">Bimodal pipeline using SBERT for retrival and T5 for generation.</p>
        </header>

        <div className="max-w-3xl mx-auto">
          <SearchBar
            mode={mode}
            setMode={setMode}
            engine={engine}
            setEngine={setEngine}
            query={activeQuery}
            setQuery={setActiveQuery}
            handleSearch={performSearch}
          />
        </div>

        {/* ERROR DISPLAY */}
        {error && <div className="p-4 bg-red-50 text-red-700 rounded-lg border border-red-200">{error}</div>}

        { /* RESULTS SECTION */}
        <div className="mt-8">
          {isLoading ? (
            <div className="flex flex-col items-center justify-center py-20">
              <RefreshCw className="animate-spin text-fuchsia-600 w-12 h-12 mb-4" />
              <p className="text-gray-500 animate-pulse">Sniffing...</p>
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
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {searchMatches.map((match) => (
                    <ResultCard key={match.embedding_id} result={match} />
                  ))}
                </div>
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