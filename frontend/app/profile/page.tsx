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
        return <div className="min-h-screen flex items-center justify-center bg-gray-50 text-xl font-bold">Please log in to view your profile.</div>;
    }

    return (
        <div className="min-h-screen bg-gray-50 pb-20">
            <div className="max-w-5xl mx-auto px-6 pt-12">
                <Link href="/" className="inline-flex items-center text-sm font-semibold text-fuchsia-600 hover:text-fuchsia-800 mb-8 transition">
                    <ArrowLeft className="w-4 h-4 mr-2" /> Back to Search
                </Link>

                <div className="bg-white rounded-3xl shadow-xl border border-gray-100 overflow-hidden">
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
                                <p className="text-gray-500 text-lg font-medium">Not enough data to map your DNA.</p>
                                <p className="text-gray-400 text-sm mt-2">Favorite a few fragrances on the search page to generate your chart!</p>
                            </div>
                        ) : (
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
                                
                                {/* Left Side: Analytical Insights */}
                                <div className="space-y-8">
                                    <div>
                                        <h3 className="text-xl font-bold text-gray-900 mb-3 flex items-center gap-2">
                                            <TrendingUp className="w-5 h-5 text-fuchsia-500" /> Olfactory Analysis
                                        </h3>
                                        <p className="text-gray-500 text-sm leading-relaxed">
                                            Based on the <strong>{favoriteIds.size}</strong> fragrances in your collection, we've unpivoted the molecular accords to map your primary scent affinities. Your collection shows a strong preference for these dominant notes:
                                        </p>
                                    </div>

                                    <div className="space-y-3">
                                        {profileData.slice(0, 3).map((item, idx) => (
                                            <div key={item.subject} className="flex items-center justify-between p-4 bg-gray-50 rounded-2xl border border-gray-100 hover:border-fuchsia-200 transition-colors">
                                                <div className="flex items-center gap-4">
                                                    <span className="flex items-center justify-center w-8 h-8 rounded-full bg-white border border-gray-200 text-fuchsia-600 font-bold text-sm shadow-sm">
                                                        {idx + 1}
                                                    </span>
                                                    <span className="font-bold text-gray-800 tracking-wide">{item.subject}</span>
                                                </div>
                                                <span className="text-xs font-bold uppercase tracking-wider text-gray-400 bg-white px-3 py-1 rounded-full border border-gray-100">
                                                    {item.A} matches
                                                </span>
                                            </div>
                                        ))}
                                    </div>
                                </div>

                                {/* Right Side: Radar Chart */}
                                <div className="w-full h-[350px] bg-gradient-to-br from-fuchsia-50/50 to-white rounded-3xl border border-fuchsia-100/50 shadow-inner p-4 relative">
                                    <ResponsiveContainer width="100%" height="100%">
                                        <RadarChart cx="50%" cy="50%" outerRadius="65%" data={profileData}>
                                            <PolarGrid stroke="#e5e7eb" />
                                            <PolarAngleAxis dataKey="subject" tick={{ fill: '#374151', fontSize: 11, fontWeight: 700 }} />
                                            <PolarRadiusAxis angle={30} domain={[0, 'auto']} tick={false} axisLine={false} />
                                            <Tooltip 
                                                contentStyle={{ borderRadius: '16px', border: '1px solid #f3e8ff', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)' }}
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