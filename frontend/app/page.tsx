"use client";

import { useState, useEffect, useRef, Suspense } from "react";
import { useSearchParams, useRouter, usePathname } from 'next/navigation';
import { RefreshCw, Search, Sparkles, Loader2, ArrowRight } from "lucide-react";
import { useFragranceSearch } from "./hooks/useFragranceSearch";
import ResultCard from "./components/ResultCard";
import SearchBar from "./components/SearchBar";
import { useAuth } from "./context/AuthContext";
import SkeletonCard from "./components/SkeletonCard";

function AIModelInterface() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const hasHydrated = useRef(false);
  const [pendingAutoSearch, setPendingAutoSearch] = useState(false);

  const { isAuthenticated } = useAuth();

  const {
    mode, setMode,
    engine, setEngine,
    smellQuery, setSmellQuery,
    notesQuery, setNotesQuery,
    isLoading, searchMatches, descriptionResult,
    performSearch, showScores, setShowScores,
    favoriteIds, toggleFavorite, currentPage, totalPages
  } = useFragranceSearch();

  // read url and trigger state updates
  useEffect(() => {
    const urlMode = searchParams.get('mode');
    const urlNotes = searchParams.get('notes');
    const urlSmell = searchParams.get('smell');
    const urlEngine = searchParams.get('engine');

    if (urlMode && !hasHydrated.current) {
      if (urlMode === 'notes_to_smell' || urlMode === 'smell_to_notes') setMode(urlMode);
      if (urlEngine) setEngine(urlEngine as any);

      if (urlMode === 'notes_to_smell' && urlNotes) {
        setNotesQuery(urlNotes);
        if (!descriptionResult) setPendingAutoSearch(true);
      } else if (urlMode === 'smell_to_notes' && urlSmell) {
        setSmellQuery(urlSmell);
        if (searchMatches.length === 0) setPendingAutoSearch(true);
      }
    }
  }, [searchParams, descriptionResult, searchMatches.length, setEngine, setMode, setNotesQuery, setSmellQuery]);

  // fire search after react finished
  useEffect(() => {
    if (pendingAutoSearch) {
      const urlNotes = searchParams.get('notes');
      const urlSmell = searchParams.get('smell');

      // Mathematically verify the input box matches the URL before searching
      const isNotesReady = mode === 'notes_to_smell' && notesQuery === urlNotes;
      const isSmellReady = mode === 'smell_to_notes' && smellQuery === urlSmell;

      if (isNotesReady || isSmellReady) {
        hasHydrated.current = true;
        setPendingAutoSearch(false);
        performSearch(1);
      }
    }
  }, [pendingAutoSearch, notesQuery, smellQuery, mode, performSearch, searchParams]);

  // update the URL when the user hits search
  const executeSearchWithUrl = () => {
    const params = new URLSearchParams(searchParams.toString());
    params.set('mode', mode);
    if (mode === 'notes_to_smell') {
      params.set('notes', notesQuery);
      params.delete('smell');
    } else {
      params.set('smell', smellQuery);
      params.set('engine', engine);
      params.delete('notes');
    }
    router.push(`${pathname}?${params.toString()}`);

    performSearch(1);
  };

  // takes t5 output and feeds it into SBERT
  const handleBridgeSearch = () => {
      if (!descriptionResult) return;
      setMode('smell_to_notes');
      setSmellQuery(descriptionResult.description);
      
      const params = new URLSearchParams(searchParams.toString());
      params.set('mode', 'smell_to_notes');
      params.set('smell', descriptionResult.description);
      params.set('engine', engine);
      params.delete('notes');
      router.push(`${pathname}?${params.toString()}`);
      
      // Let our robust useEffect handle the synchronized execution!
      setPendingAutoSearch(true);
  }

  // determine active query based on mode
  const activeQuery = mode === 'notes_to_smell' ? notesQuery : smellQuery;
  const setActiveQuery = mode === 'notes_to_smell' ? setNotesQuery : setSmellQuery;

  // typewriter effect for the hero subtitle
  const searchExamples = [
    "old dusty library books...",
    "warm cashmere by a fireplace...",
    "smoky leather and dark rum...",
    "fresh rain on concrete...",
    "citrusy bergamot and lavender...",
    "old jazz club with a hint of mystery..."
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

  // note chips, to avoid blank page
  const popularNotes = ['Bergamot', 'Jasmine', 'Musk', 'Patchouli', 'Vanilla', 'Sandalwood', 'Amber'];
  const surpriseCombos = [
    "black cherry, bitter almond, tonka bean", 
    "cherry, nectarine, red apple, pear, pineapple, litchi, peony, watermelon, lotus, cyclamen, jasmine, praline, sandalwood, amber, virginia cedar",
    "green mandarin, mandarin orange, jasmine, neroli, amber, musk",  
    "raspberry, pink pepper, orange blossom, white flowers, iris, black vanilla husk, benzoin",
    "cardamom, sandalwood, violet, leather"    
  ];

  return (
    <div className="min-h-screen bg-zinc-950 font-sans text-zinc-200 pb-20">

      {/* Hero Section (Dark with Radial Gradient) */}
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

      {/* Main Content Area (Overlapping the Hero) */}
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
            handleSearch={executeSearchWithUrl}
          />
          
          {/* note chips */}
          {mode === 'notes_to_smell' && (
             <div className="mt-4 flex flex-wrap items-center justify-center gap-2 animate-in fade-in slide-in-from-top-2 duration-300">
                <span className="text-sm font-semibold text-zinc-500 mr-1">Try adding:</span>
                {popularNotes.map(note => (
                    <button 
                        key={note} 
                        onClick={() => setNotesQuery(prev => prev ? `${prev}, ${note}` : note)} 
                        className="px-3 py-1 bg-zinc-800 border border-zinc-700 rounded-full text-xs font-medium text-zinc-300 hover:border-fuchsia-500/50 hover:text-fuchsia-400 transition-all"
                    >
                        + {note}
                    </button>
                ))}
                <button 
                    onClick={() => setNotesQuery(surpriseCombos[Math.floor(Math.random() * surpriseCombos.length)])} 
                    className="px-3 py-1 bg-fuchsia-500/15 border border-fuchsia-500/30 rounded-full text-xs font-bold text-fuchsia-400 hover:bg-fuchsia-500/25 transition-all flex items-center"
                >
                    <Sparkles className="w-3 h-3 mr-1" /> Surprise Me
                </button>
             </div>
          )}
        </div>

        { /* 3. RESULTS SECTION */}
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
                <div className="max-w-3xl mx-auto bg-gradient-to-br from-fuchsia-500/10 to-zinc-900 p-8 rounded-2xl border border-fuchsia-500/20">
                  <div className="flex items-center gap-2 mb-4 text-fuchsia-400 font-bold uppercase tracking-widest text-xs">
                    <Sparkles size={18} /> Description
                  </div>
                  <p className="text-2xl text-zinc-200 italic font-serif leading-relaxed"> "{descriptionResult.description}" </p>

                  {/* the bridge button */}
                  <div className="pt-6 border-t border-fuchsia-500/20 flex justify-end">
                      <button
                          onClick={handleBridgeSearch}
                          className="flex items-center gap-2 px-6 py-2.5 bg-fuchsia-600 text-white rounded-xl font-semibold text-sm hover:bg-fuchsia-700 hover:shadow-lg hover:-translate-y-0.5 transition-all duration-200"
                      >
                          <Search className="w-4 h-4" /> Find perfumes with this vibe <ArrowRight className="w-4 h-4" />
                      </button>
                  </div>
                </div>
              )}

              {/* SBERT OUTPUT (THE MARKETPLACE GRID) */}
              {mode === 'smell_to_notes' && searchMatches.length > 0 && (
                <>
                  <div className="flex justify-between items-end mb-6">
                    <h2 className="text-2xl font-extrabold text-zinc-100 tracking-tight">Results</h2>
                    <button
                      onClick={() => setShowScores(s => !s)}
                      className="text-xs font-semibold text-zinc-400 hover:text-fuchsia-400 flex items-center gap-2 transition px-3 py-1.5 rounded-full bg-zinc-800 border border-zinc-700 hover:border-fuchsia-500/40"
                    >
                      <span className={`w-8 h-4 rounded-full transition-colors duration-200 flex items-center px-0.5 ${showScores ? 'bg-fuchsia-500' : 'bg-zinc-600'}`}>
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
                    <div className="flex items-center justify-center space-x-6 mt-12 pt-8 border-t border-zinc-800">
                      <button
                        onClick={() => {
                          performSearch(currentPage - 1);
                          window.scrollTo({ top: 0, behavior: 'smooth' });
                        }}
                        disabled={currentPage === 1 || isLoading}
                        className="px-5 py-2 rounded-xl font-semibold text-sm transition-all disabled:opacity-40 disabled:cursor-not-allowed bg-zinc-800 border border-zinc-700 text-zinc-300 hover:text-fuchsia-400 hover:border-fuchsia-500/40"
                      >
                        &larr; Previous
                      </button>
                      <span className="text-sm font-medium text-zinc-400 bg-zinc-800 px-4 py-1.5 rounded-full border border-zinc-700">
                        Page <strong className="text-zinc-100">{currentPage}</strong> of <strong className="text-zinc-100">{totalPages}</strong>
                      </span>
                      <button
                        onClick={() => {
                          performSearch(currentPage + 1);
                          window.scrollTo({ top: 0, behavior: 'smooth' });
                        }}
                        disabled={currentPage === totalPages || isLoading}
                        className="px-5 py-2 rounded-xl font-semibold text-sm transition-all disabled:opacity-40 disabled:cursor-not-allowed bg-zinc-800 border border-zinc-700 text-zinc-300 hover:text-fuchsia-400 hover:border-fuchsia-500/40"
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
                  <div className="text-center py-24 border-2 border-dashed border-zinc-800 rounded-3xl bg-zinc-900/50">
                    <div className="w-16 h-16 bg-zinc-800 rounded-full flex items-center justify-center mx-auto mb-4">
                      <Search className="w-8 h-8 text-zinc-600" />
                    </div>
                    <h3 className="text-lg font-bold text-zinc-200 mb-1">Ready to explore</h3>
                    <p className="text-zinc-400 max-w-md mx-auto">Enter fragrance notes or describe a scent to begin searching the catalog.</p>
                  </div>
                )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function Page() {
  return (
    <Suspense fallback={
      <div className="min-h-screen flex items-center justify-center bg-zinc-950">
        <Loader2 className="w-8 h-8 animate-spin text-fuchsia-600" />
      </div>
    }>
      <AIModelInterface />
    </Suspense>
  );
}