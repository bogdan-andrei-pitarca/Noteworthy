"use client";

import { useState } from "react";
import { Send, Search, Zap, RefreshCw, FileText } from "lucide-react";

export default function AIModelInterface() {
  const [description, setDescription] = useState("");
  const [notes, setNotes] = useState("");
  const [loading, setLoading] = useState({ sbert: false, t5: false });
  // so we can trigger sbert and t5 calls separately
  // when SBERT starts, for example, we call setLoading({ ...loading, sbert: true });
  // the spread operator keeps the other loading state unchanged
  const [result, setResult] = useState({ noteMatch: "", expandedDesc: ""});
  // result.noteMatch holds SBERT output
  // result.expandedDesc holds T5 output

  const handleSBERT = async () => {
    setLoading({ ...loading, sbert: true });
    // TODO: call SBERT API
    // const res = await fetch('/api/sbert', { method: 'POST', body: JSON.stringify({ description }) });
    setLoading({ ...loading, sbert: false });
  }

  const handleT5 = async () => {
    setLoading({ ...loading, t5: true });
    // TODO: call T5 API
    // const res = await fetch('/api/t5', { method: 'POST', body: JSON.stringify({ notes }) });
    setLoading({ ...loading, t5: false });
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8 font-sans text-gray-800">
      <div className="max-w-5xl mx-auto bg-white p-6 rounded-xl shadow-lg space-y-8">
        <header className="border-b pb-6">
          <h1 className="text-3xl font-extrabold tracking-tight text-fuschia-800 mb-2">Fragrance Text Processor</h1>
          <p className="text-gray-600 text-lg mt-2">Bimodal pipeline using SBERT for retrival and T5 for generation.</p>
        </header>
        
        <div className="grid md:grid-cols-2 gap-8">
          { /* SBERT Section: DESC -> NOTES */ }
          <section className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 flex flex-col">
            <div className="flex items-center gap-2 mb-4 text-blue-600">
              <Search className="w-5 h-5" size={20} />
              <h2 className="font-semibold text-lg">SBERT: Description to Notes</h2>
            </div>
            <p className="text-sm text-gray-500 mb-4">Input a fragrance description and retrieve the most similar fragrance notes using vector embeddings.</p>
          
            <textarea
              className="flex-1 w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none min-h-[200px] text-sm"
              placeholder="Enter a fragrance description here..."
              value={description} 
              onChange={(e) => setDescription(e.target.value)}
            />

            <button
              onClick={handleSBERT}
              disabled={loading.sbert}
              className="mt-4 w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 rounded-lg flex items-center justify-center gap-2 transition-colors disabled:opacity-50"
              >
                {loading.sbert ? <RefreshCw className="animate-spin" size={18} /> : <Zap size={18} />}
                Process with SBERT
                </button>
          </section>

          { /* T5 Section: NOTES -> DESC */ }
          <section className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 flex flex-col">
            <div className="flex items-center gap-2 mb-4 text-green-600">
              <FileText className="w-5 h-5" size={20} />
              <h2 className="font-semibold text-lg">T5: Text Generation</h2>
            </div>
            <p className="text-sm text-gray-500 mb-4">Expand notes into descriptions.</p>

            <textarea
              className="flex-1 w-full p-3 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none min-h-[200px] text-sm"
              placeholder="Enter fragrance notes here..."
              value={notes} 
              onChange={(e) => setNotes(e.target.value)}
            />

            <button
              onClick={handleT5}
              disabled={loading.t5}
              className="mt-4 w-full bg-green-600 hover:bg-green-700 text-white font-medium py-2 rounded-lg flex items-center justify-center gap-2 transition-colors disabled:opacity-50"
              >
                {loading.t5 ? <RefreshCw className="animate-spin" size={18} /> : <Send size={18} />}
                Process with T5
                </button>
          </section>
        </div>

        { /* Results Section */ }
        <div className="mt-8 bg-gray-900 rounded-xl p-6 text-gray-100 min-h-[100px] relative overflow-hidden">
          <div className="absolute top-0 right-0 p-2 opacity-10">
            <Zap size={80} />
          </div>
          <h3 className="text-xs uppercase tracking-widest text-gray-400 font-bold mb-2">Results </h3>
          <div className="text-lg">
            {result.noteMatch || result.expandedDesc ? (
              <p>{result.noteMatch || result.expandedDesc}</p>
            ) : (
                <span className="text-gray-500 italic">Processed results will appear here...</span>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}