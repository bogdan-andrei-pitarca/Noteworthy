"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { fragranceService } from "@/app/services";
import { FragranceRecord } from "@/app/types/FragranceTypes";
import { Sparkles, ExternalLink, ArrowLeft, Loader2 } from "lucide-react";
import Link from "next/link";
import ResultCard from "@/app/components/ResultCard"; 

export default function FragranceDetail() {
    const params = useParams();
    const id = Number(params.id);

    const [fragrance, setFragrance] = useState<FragranceRecord | null>(null);
    const [aiDescription, setAiDescription] = useState<string | null>(null);
    const [similar, setSimilar] = useState<FragranceRecord[]>([]); 
    const [isLoading, setIsLoading] = useState(true);
    const [isGenerating, setIsGenerating] = useState(true);

    // fetch the basic details
    useEffect(() => {
        const fetchDetails = async () => {
            try {
                const data = await fragranceService.getFragranceById(id);
                setFragrance(data);
                
                // fetch similar fragrances in parallel
                fragranceService.getSimilarFragrances(id)
                    .then(setSimilar)
                    .catch(console.error);
                
                // trigger the T5 generation
                if (data.all_notes) {
                    const descData = await fragranceService.generateDescription(data.all_notes);
                    setAiDescription(descData.description);
                }
            } catch (error) {
                console.error("Error fetching details:", error);
            } finally {
                setIsLoading(false);
                setIsGenerating(false);
            }
        };

        if (id) fetchDetails();
    }, [id]);

    if (isLoading) {
        return <div className="min-h-screen flex items-center justify-center bg-gray-50"><Loader2 className="w-8 h-8 animate-spin text-fuchsia-600" /></div>;
    }

    if (!fragrance) {
        return <div className="min-h-screen flex items-center justify-center bg-gray-50 text-xl font-bold">Fragrance not found.</div>;
    }

    // clean up accords for display
    const accords = [
        fragrance.main_accord_1, fragrance.main_accord_2, fragrance.main_accord_3, 
        fragrance.main_accord_4, fragrance.main_accord_5
    ].filter(a => a && a.toLowerCase() !== 'none');

    // clean up notes array string
    const cleanNotes = fragrance.all_notes.replace(/['\[\]]/g, '').split(',').map(n => n.trim());

    return (
        <div className="min-h-screen bg-gray-50 pb-20">
            <div className="max-w-4xl mx-auto px-6 pt-12">
                <Link href="/" className="inline-flex items-center text-sm font-semibold text-fuchsia-600 hover:text-fuchsia-800 mb-8 transition">
                    <ArrowLeft className="w-4 h-4 mr-2" /> Back to Search
                </Link>

                <div className="bg-white rounded-3xl shadow-xl border border-gray-100 overflow-hidden">
                    {/* Header Section */}
                    <div className="bg-zinc-950 px-8 py-6 text-white relative">
                        <a href={fragrance.url} target="_blank" rel="noopener noreferrer" className="absolute top-6 right-6 p-3 bg-white/10 hover:bg-white/20 rounded-full transition">
                            <ExternalLink className="w-5 h-5 text-white" />
                        </a>
                        <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight capitalize mb-2">
                            {fragrance.perfume_name.replace(/-/g, ' ')}
                        </h1>
                        <p className="text-lg text-zinc-400 font-medium capitalize">
                            by {fragrance.brand.replace(/-/g, ' ')} {fragrance.launch_year ? `(${fragrance.launch_year})` : ''}
                        </p>
                        
                        <div className="flex flex-wrap gap-2 mt-4">
                            {accords.map(accord => (
                                <span key={accord} className="px-3 py-1 text-xs font-bold tracking-wide rounded-md bg-white/10 text-zinc-200 border border-white/20 uppercase">
                                    {accord}
                                </span>
                            ))}
                        </div>
                    </div>

                    <div className="p-8">
                        {/* T5 Generative Section */}
                        <div className="mb-8 p-6 bg-gradient-to-br from-fuchsia-50 to-white rounded-2xl border border-fuchsia-100 shadow-sm relative overflow-hidden"> 
                            <div className="flex items-center gap-2 mb-3 text-fuchsia-700 font-bold uppercase tracking-widest text-xs">
                                <Sparkles size={16} /> Noteworthy AI Interpretation
                            </div>
                            {isGenerating ? (
                                <div className="flex items-center text-fuchsia-600 italic">
                                    <Loader2 className="w-4 h-4 mr-2 animate-spin" /> Analyzing notes and generating description...
                                </div>
                            ) : (
                                <p className="text-xl text-gray-800 italic font-serif leading-relaxed"> 
                                    "{aiDescription}"
                                </p>
                            )}
                        </div>

                        {/* Data Grid */}
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                            <div className="md:col-span-2">
                                <h3 className="text-base font-bold text-gray-900 mb-3 border-b pb-2">Complete Note Pyramid</h3>
                                <div className="flex flex-wrap gap-2">
                                    {cleanNotes.map((note, i) => (
                                        <span key={i} className="px-3 py-1 bg-gray-100 text-gray-700 rounded-lg text-sm font-medium capitalize">
                                            {note}
                                        </span>
                                    ))}
                                </div>
                            </div>
                            
                            <div>
                                <h3 className="text-base font-bold text-gray-900 mb-3 border-b pb-2">Details</h3>
                                <ul className="space-y-2 text-sm">
                                    <li className="flex justify-between"><span className="text-gray-500">Gender</span> <span className="font-semibold text-gray-900 capitalize">{fragrance.gender}</span></li>
                                    <li className="flex justify-between"><span className="text-gray-500">Rating</span> <span className="font-semibold text-gray-900">{fragrance.rating_value} / 5</span></li>
                                    <li className="flex justify-between"><span className="text-gray-500">Reviews</span> <span className="font-semibold text-gray-900">{fragrance.rating_count?.toLocaleString()}</span></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>

                {/* "more like this" section */}
                {similar.length > 0 && (
                    <div className="mt-12">
                        <h2 className="text-2xl font-extrabold text-gray-900 tracking-tight mb-6 flex items-center gap-2">
                            You Might Also Like
                        </h2>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            {similar.map((match, index) => (
                                <ResultCard
                                    key={match.embedding_id}
                                    result={match}
                                    index={index + 1} // offset so we don't trigger the "Perfect Match" badge
                                    showScores={false}
                                />
                            ))}
                        </div>
                    </div>
                )}

            </div>
        </div>
    );
}