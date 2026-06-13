"use client";

import { useEffect, useState } from "react";
import { useFragranceSearch } from "@/app/hooks/useFragranceSearch";
import { fragranceService } from "@/app/services";
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip } from "recharts";
import { Loader2, ArrowLeft, Hexagon, TrendingUp } from "lucide-react";
import Link from "next/link";
import { useAuth } from "@/app/context/AuthContext";

export default function ProfilePage() {
    const { isAuthenticated } = useAuth();
    const { favoriteIds } = useFragranceSearch();
    const [profileData, setProfileData] = useState<any[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchProfile = async () => {
            if (favoriteIds.size === 0) {
                setIsLoading(false);
                return;
            }
            try {
                // Convert the Set to an Array for the API
                const data = await fragranceService.getScentProfile(Array.from(favoriteIds));
                setProfileData(data);
            } catch (error) {
                console.error("Error fetching profile:", error);
            } finally {
                setIsLoading(false);
            }
        };

        if (isAuthenticated) {
            fetchProfile();
        } else {
            setIsLoading(false);
        }
    }, [favoriteIds, isAuthenticated]);

    if (!isAuthenticated) {
        return <div className="min-h-screen flex items-center justify-center bg-zinc-950 text-xl font-bold text-zinc-200">Please log in to view your profile.</div>;
    }

    return (
        <div className="min-h-screen bg-zinc-950 pb-20">
            <div className="max-w-5xl mx-auto px-6 pt-12">
                <Link href="/" className="inline-flex items-center text-sm font-semibold text-fuchsia-600 hover:text-fuchsia-400 mb-8 transition">
                    <ArrowLeft className="w-4 h-4 mr-2" /> Back to Search
                </Link>

                <div className="bg-zinc-900 rounded-3xl shadow-xl border border-zinc-800 overflow-hidden">
                    {/* Header */}
                    <div className="bg-zinc-950 px-8 py-8 text-white text-center relative overflow-hidden">
                        <div className="absolute top-0 left-0 w-full h-full bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-fuchsia-900/20 via-zinc-950 to-zinc-950"></div>
                        <div className="relative z-10">
                            <Hexagon className="w-12 h-12 text-fuchsia-400 mx-auto mb-4" />
                            <h1 className="text-3xl font-extrabold tracking-tight mb-2">Your Scent DNA</h1>
                            <p className="text-zinc-400 font-medium max-w-lg mx-auto">
                                Take a look at your preferences!
                            </p>
                        </div>
                    </div>

                    <div className="p-8 md:p-12">
                        {isLoading ? (
                            <div className="flex justify-center py-20"><Loader2 className="w-8 h-8 animate-spin text-fuchsia-600" /></div>
                        ) : profileData.length === 0 ? (
                            <div className="text-center py-20">
                                <p className="text-zinc-400 text-lg font-medium">Not enough data to map your DNA.</p>
                                <p className="text-zinc-500 text-sm mt-2">Favorite a few fragrances on the search page to generate your chart!</p>
                            </div>
                        ) : (
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
                                
                                {/* Left Side: Analytical Insights */}
                                <div className="space-y-8">
                                    <div>
                                        <h3 className="text-xl font-bold text-zinc-100 mb-3 flex items-center gap-2">
                                            <TrendingUp className="w-5 h-5 text-fuchsia-500" /> Olfactory Analysis
                                        </h3>
                                        <p className="text-zinc-400 text-sm leading-relaxed">
                                            Based on the <strong className="text-zinc-200">{favoriteIds.size}</strong> fragrances in your collection, we've unpivoted the molecular accords to map your primary scent affinities. Your collection shows a strong preference for these dominant notes:
                                        </p>
                                    </div>

                                    <div className="space-y-3">
                                        {profileData.slice(0, 3).map((item, idx) => (
                                            <div key={item.subject} className="flex items-center justify-between p-4 bg-zinc-800 rounded-2xl border border-zinc-700 hover:border-fuchsia-500/40 transition-colors">
                                                <div className="flex items-center gap-4">
                                                    <span className="flex items-center justify-center w-8 h-8 rounded-full bg-zinc-900 border border-zinc-700 text-fuchsia-400 font-bold text-sm">
                                                        {idx + 1}
                                                    </span>
                                                    <span className="font-bold text-zinc-200 tracking-wide">{item.subject}</span>
                                                </div>
                                                <span className="text-xs font-bold uppercase tracking-wider text-zinc-400 bg-zinc-900 px-3 py-1 rounded-full border border-zinc-700">
                                                    {item.A} matches
                                                </span>
                                            </div>
                                        ))}
                                    </div>
                                </div>

                                {/* Right Side: Radar Chart */}
                                <div className="w-full h-[350px] bg-gradient-to-br from-fuchsia-500/5 to-zinc-900 rounded-3xl border border-zinc-800 shadow-inner p-4 relative">
                                    <ResponsiveContainer width="100%" height="100%">
                                        <RadarChart cx="50%" cy="50%" outerRadius="65%" data={profileData}>
                                            <PolarGrid stroke="#3f3f46" />
                                            <PolarAngleAxis dataKey="subject" tick={{ fill: '#a1a1aa', fontSize: 11, fontWeight: 700 }} />
                                            <PolarRadiusAxis angle={30} domain={[0, 'auto']} tick={false} axisLine={false} />
                                            <Tooltip 
                                                contentStyle={{ borderRadius: '16px', background: '#18181b', border: '1px solid #3f3f46', color: '#e4e4e7', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.3)' }}
                                                formatter={(value) => [`${value} matching accords`, 'Frequency']}
                                            />
                                            <Radar
                                                name="Olfactory Preference"
                                                dataKey="A"
                                                stroke="#d946ef"
                                                strokeWidth={2}
                                                fill="#d946ef"
                                                fillOpacity={0.3}
                                            />
                                        </RadarChart>
                                    </ResponsiveContainer>
                                </div>

                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}